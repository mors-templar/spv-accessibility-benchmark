#!/usr/bin/env python3
"""Serve masked exploratory review copies on loopback-only ports."""

import argparse
import functools
import html
import http.server
import json
import re
import sys
import threading
from pathlib import Path

import prepare_review_cases as review
import audit_initial_state as audit
import run_codex_development as development


def review_html(rows):
    body = []
    for row in rows:
        case_id = html.escape(row["case_id"])
        task_id = html.escape(row["task_id"])
        if row["url"] is None:
            link = "<span>Not available as a static page</span>"
        else:
            link = f'<a href="{html.escape(row["url"], quote=True)}">Open {case_id}</a>'
        body.append(f"<tr><th scope=\"row\">{case_id}</th><td>{task_id}</td><td>{link}</td></tr>")
    table = "\n".join(body)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Exploratory accessibility review</title>
<style>
body{{font:1rem/1.5 system-ui,sans-serif;color:#172a37;background:#f5f8fa;margin:0}}
main{{max-width:70rem;margin:auto;padding:2rem 1rem}} h1{{line-height:1.2}}
.notice{{background:#fff;border-left:0.3rem solid #145b78;padding:1rem}}
table{{border-collapse:collapse;width:100%;background:#fff}} th,td{{padding:.7rem;text-align:left;border:1px solid #8a9ba6}}
a{{color:#004a77}} a:focus-visible{{outline:3px solid #ad4000;outline-offset:3px}}
.scroll{{overflow-x:auto}} caption{{font-weight:700;text-align:left;padding:.5rem 0}}
</style></head><body><main><h1>Exploratory accessibility review</h1>
<p class="notice">Condition labels are hidden in this view. Site content and prior knowledge can still reveal them.
These are development artifacts, not final benchmark results. Some cases have no static page to review.</p>
<div class="scroll"><table><caption>Review cases</caption><thead><tr><th scope="col">Case</th>
<th scope="col">Task</th><th scope="col">Page</th></tr></thead><tbody>{table}</tbody></table></div>
<p>Use the manual review form and record untested or unavailable checks. Do not repair the source artifact during review.</p>
</main></body></html>"""


class CaseHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        requested = Path(self.translate_path(self.path)).resolve()
        root = Path(self.directory).resolve()
        if not requested.is_relative_to(root) or requested.name.lower() in review.PRIVATE_SIDECARS:
            self.send_error(404)
            return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404)
        return None

    def log_message(self, format, *args):
        pass


class HubHandler(http.server.BaseHTTPRequestHandler):
    content = b""

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self.content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(self.content)

    def log_message(self, format, *args):
        pass


def verified_site(case):
    if not re.fullmatch(r"CASE-\d{2}", case["case_id"]):
        raise ValueError("Invalid case ID.")
    site = review.REVIEW_ROOT / "cases" / case["case_id"] / "site"
    actual = development.artifact_manifest(site)["files"]
    if actual != case["included_files"] or not (site / "index.html").is_file():
        raise ValueError("A review copy differs from its recorded files.")
    return site


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        raise ValueError("Port must be between 1 and 65535.")
    mapping = json.loads((review.REVIEW_ROOT / "private-mapping.json").read_text(encoding="utf-8"))
    if mapping["status"] not in {"prepared_with_gaps", "all_static_copies_ready"}:
        raise ValueError("Review cases have not finished preparation.")
    servers = []
    threads = []
    rows = []
    try:
        for case in mapping["cases"]:
            row = {"case_id": case["case_id"], "task_id": case["task_id"], "url": None}
            if case["status"] == "ready_static_copy":
                site = verified_site(case)
                handler = functools.partial(CaseHandler, directory=str(site))
                server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                servers.append(server)
                threads.append(thread)
                row["url"] = f"http://127.0.0.1:{server.server_port}/"
            rows.append(row)
        HubHandler.content = review_html(rows).encode("utf-8")
        index = review.REVIEW_ROOT / "index.html"
        index_hash = review.REVIEW_ROOT / "index.sha256"
        if index.exists() and (not index_hash.is_file() or index_hash.read_text(encoding="utf-8").strip() != audit.sha256_file(index)):
            raise FileExistsError("The existing review index was changed; do not overwrite it.")
        if not index.exists() and index_hash.exists():
            raise FileExistsError("The review index hash exists without its file; do not overwrite it.")
        index.write_bytes(HubHandler.content)
        index_hash.write_text(audit.sha256_file(index) + "\n", encoding="utf-8")
        hub = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), HubHandler)
        print(f"Review index: http://127.0.0.1:{args.port}/", flush=True)
        try:
            hub.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            hub.server_close()
    finally:
        for server in servers:
            server.shutdown()
            server.server_close()
        for thread in threads:
            thread.join(timeout=5)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
