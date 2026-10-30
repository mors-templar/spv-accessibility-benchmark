"""Build local study-plan diagrams and a readable HTML copy of the draft."""

from pathlib import Path
import html
import textwrap

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["svg.hashsalt"] = "spv-study-plan-v01"
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import markdown


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "diagrams"
INK = "#112d42"
SUB = "#35566c"
LINE = "#9aaeb7"
BLUE = "#e8f1f8"
TEAL = "#d9f1ed"
GOLD = "#fff0d4"
ROSE = "#fbe9e2"
PALE = "#f5f8f8"


def canvas(title, subtitle, size=(16, 9)):
    fig, ax = plt.subplots(figsize=size)
    fig.patch.set_facecolor("white")
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    ax.text(0.04, 0.96, title, fontsize=24, color=INK, weight="bold", va="top")
    ax.text(0.04, 0.91, subtitle, fontsize=12.5, color=SUB, va="top")
    return fig, ax


def box(ax, x, y, w, h, title, body, color, title_size=13, body_size=11):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.008,rounding_size=0.012",
        facecolor=color, edgecolor="#b8ccd2", linewidth=1,
    )
    ax.add_patch(rect)
    ax.text(x + 0.014, y + h - 0.018, title, color=INK,
            fontsize=title_size, weight="bold", va="top")
    ax.text(x + 0.014, y + h - 0.055, body, color=SUB,
            fontsize=body_size, va="top", linespacing=1.3)


def arrow(ax, start, end, color=LINE, connection="arc3"):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=13,
        linewidth=1.35, color=color, connectionstyle=connection,
    ))


def save(fig, stem):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / f"{stem}.png", dpi=170, bbox_inches="tight", facecolor="white")
    svg = OUT / f"{stem}.svg"
    fig.savefig(svg, bbox_inches="tight", facecolor="white", metadata={"Date": None})
    content = svg.read_text(encoding="utf-8")
    svg.write_text("\n".join(line.rstrip() for line in content.splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def architecture():
    fig, ax = canvas("Study architecture", "Five fixed requests. Six conditions. One independent evaluation.")
    box(ax, 0.30, 0.75, 0.40, 0.12, "FIVE SELECTED WEBSITE REQUESTS",
        "Same original task text in each condition", BLUE, 14, 11.5)
    arms = [
        ("B  BASELINE", "Original task\nonly", PALE),
        ("D  CHECKLIST", "Task + full\nchecklist", BLUE),
        ("P  PROMPT", "Checklist +\nplan guidance", TEAL),
        ("S  SKILL", "Checklist +\nskill and tool", TEAL),
        ("A  AGENT", "Checklist +\nreview gate", GOLD),
        ("X  COMBINED", "Checklist + P\n+ S + A", ROSE),
    ]
    left, gap, width = 0.04, 0.014, 0.142
    for i, (title, body, color) in enumerate(arms):
        x = left + i * (width + gap)
        box(ax, x, 0.50, width, 0.15, title, body, color, 11.5, 10.5)
        arrow(ax, (0.50, 0.75), (x + width / 2, 0.65))
        arrow(ax, (x + width / 2, 0.50), (0.50, 0.40))
    box(ax, 0.30, 0.32, 0.40, 0.08, "PRESERVE EACH ATTEMPT",
        "Site or failure, input hashes, and process logs", PALE, 13, 10.5)
    cols = [
        (0.04, "TASK FUNCTION", "Required user journeys"),
        (0.36, "BROWSER + AXE", "Automated checks and states"),
        (0.68, "HUMAN REVIEW", "Keyboard, visual, and context"),
    ]
    for x, title, body in cols:
        box(ax, x, 0.14, 0.28, 0.11, title, body, BLUE, 12, 10.5)
        arrow(ax, (0.50, 0.32), (x + 0.14, 0.25))
    ax.text(0.50, 0.06, "Report outcomes, unknowns, failures, and costs by task and condition.",
            fontsize=12, color=INK, ha="center", weight="bold")
    save(fig, "01-study-architecture")


def matrix():
    fig, ax = canvas("Condition matrix", "The task text stays fixed. Added components are the treatment.", (16, 8.5))
    left = 0.04
    widths = [0.18, 0.19, 0.19, 0.19, 0.19]
    labels = ["CONDITION", "FULL CHECKLIST", "PLAN GUIDANCE", "SKILL", "REVIEW GATE"]
    xs = [left]
    for width in widths[:-1]:
        xs.append(xs[-1] + width)
    for x, width, label in zip(xs, widths, labels):
        ax.add_patch(FancyBboxPatch((x, 0.755), width - 0.006, 0.07,
                     boxstyle="round,pad=0.003,rounding_size=0.006",
                     facecolor="#dceaf1", edgecolor="none"))
        ax.text(x + width / 2 - 0.003, 0.79, label, ha="center", va="center",
                fontsize=10.5, color=INK, weight="bold")
    rows = [
        ("B  Baseline", False, False, False, False),
        ("D  Checklist", True, False, False, False),
        ("P  Prompt", True, True, False, False),
        ("S  Skill", True, False, True, False),
        ("A  Agent", True, False, False, True),
        ("X  Combined", True, True, True, True),
    ]
    for row, record in enumerate(rows):
        y = 0.64 - row * 0.085
        ax.text(xs[0] + 0.015, y + 0.033, record[0], color=INK,
                fontsize=12, weight="bold", va="center")
        for col, value in enumerate(record[1:], start=1):
            ax.add_patch(FancyBboxPatch((xs[col], y), widths[col] - 0.006, 0.067,
                         boxstyle="round,pad=0.003,rounding_size=0.006",
                         facecolor=TEAL if value else PALE, edgecolor="none"))
            ax.text(xs[col] + widths[col] / 2 - 0.003, y + 0.033,
                    "INCLUDED" if value else "ABSENT", ha="center", va="center",
                    color="#07584f" if value else "#657c88", fontsize=11,
                    weight="bold" if value else "normal")
    ax.text(0.04, 0.09, "Every row also includes the unchanged original task.", fontsize=12, color=INK, weight="bold")
    ax.text(0.04, 0.045, "S uses an advisory diagnostic. A and X require a host-enforced gate.", fontsize=11.5, color=SUB)
    save(fig, "02-condition-matrix")


def gate():
    fig, ax = canvas("Proposed reviewer gate", "A and X use one user submission and may make extra internal calls.")
    box(ax, 0.04, 0.57, 0.25, 0.18, "1  PLAN PHASE",
        "Generator writes a plan.\nHost denies output writes.", BLUE, 13, 11)
    box(ax, 0.365, 0.57, 0.25, 0.18, "2  REVIEW PLAN",
        "Separate reviewer checks\nquestions and planned behavior.", GOLD, 13, 11)
    box(ax, 0.69, 0.57, 0.26, 0.18, "3  APPROVED BUILD",
        "Host permits a writable phase.\nGenerator builds the site.", TEAL, 13, 11)
    arrow(ax, (0.29, 0.66), (0.365, 0.66))
    arrow(ax, (0.615, 0.66), (0.69, 0.66))
    ax.text(0.64, 0.70, "approve", fontsize=10, color=SUB)
    box(ax, 0.33, 0.25, 0.32, 0.16, "REVISE OR INSUFFICIENT EVIDENCE",
        "Return findings to the generator.\nAt most two revised plans are proposed.", ROSE, 12, 10.5)
    arrow(ax, (0.49, 0.57), (0.49, 0.41))
    arrow(ax, (0.33, 0.33), (0.165, 0.57), connection="arc3,rad=-0.25")
    box(ax, 0.72, 0.25, 0.22, 0.16, "BLOCKED",
        "Stop after the retry limit.\nKeep the failure record.", PALE, 12, 10.5)
    arrow(ax, (0.65, 0.33), (0.72, 0.33))
    ax.text(0.04, 0.10, "Plan approval is not a WCAG pass. Finished sites receive separate evaluation.",
            fontsize=12, color=INK, weight="bold")
    ax.text(0.04, 0.055, "A read-only phase can block file writes; it cannot stop a model emitting code as text.",
            fontsize=11.5, color=SUB)
    save(fig, "03-plan-gate")


def build_html():
    names = [
        "01-study-design.md", "02-prompt-pack.md", "03-evaluation.md",
        "04-build-and-run.md", "05-evidence.md",
    ]
    sources = ["<!-- Source: " + name + " -->\n\n" + (ROOT / name).read_text(encoding="utf-8") for name in names]
    converter = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
    body = converter.convert("\n\n".join(sources))
    toc = converter.toc
    title = html.escape("SPV accessibility study: draft experiment plan")
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>
:root {{ color-scheme: light; font-family: system-ui, sans-serif; color: #112d42; background: #eef3f4; }}
* {{ box-sizing: border-box; }} body {{ margin: 0; line-height: 1.65; }}
header {{ background: #112d42; color: white; padding: 1.8rem max(1rem, calc((100vw - 1450px) / 2)); }}
header h1 {{ margin: 0; font-size: clamp(1.6rem, 3vw, 2.35rem); }} header p {{ margin: .5rem 0 0; color: #d4e8ea; }}
.wrap {{ max-width: 1450px; margin: auto; display: grid; grid-template-columns: 265px minmax(0, 1fr); gap: 1.5rem; padding: 1.5rem; }}
aside {{ align-self: start; position: sticky; top: 1rem; max-height: calc(100vh - 2rem); overflow: auto; background: white; border-radius: .7rem; padding: 1rem; }}
aside strong {{ font-size: 1.05rem; }} aside ul {{ padding-left: 1.2rem; }} aside li {{ margin: .25rem 0; }} aside ul ul {{ font-size: .86rem; }}
main {{ min-width: 0; background: white; padding: clamp(1rem, 3vw, 3rem); border-radius: .7rem; }}
h1, h2, h3 {{ line-height: 1.25; color: #112d42; scroll-margin-top: 1rem; }} h1:not(:first-child) {{ margin-top: 3.5rem; padding-top: 1.5rem; border-top: 2px solid #c7d9df; }}
h2 {{ margin-top: 2.2rem; }} a {{ color: #075f78; text-underline-offset: .16em; }}
img {{ max-width: 100%; height: auto; border: 1px solid #d9e4e7; border-radius: .5rem; }}
table {{ display: block; max-width: 100%; overflow-x: auto; border-collapse: collapse; margin: 1.25rem 0; }}
th, td {{ border: 1px solid #cddce0; padding: .65rem; text-align: left; vertical-align: top; }} th {{ background: #e4eff2; }}
pre {{ overflow-x: auto; background: #102d3b; color: #eef8f8; padding: 1rem; border-radius: .4rem; line-height: 1.5; }}
code {{ font-family: ui-monospace, Consolas, monospace; }} p code, td code, li code {{ background: #edf3f4; padding: .1em .2em; }}
@media (max-width: 900px) {{ .wrap {{ display: block; padding: .75rem; }} aside {{ position: static; max-height: 18rem; margin-bottom: 1rem; }} main {{ padding: 1rem; }} }}
@media print {{ body {{ background: white; }} header {{ color: #112d42; background: white; }} header p {{ color: #35566c; }} .wrap {{ display: block; }} aside {{ display: none; }} main {{ padding: 0; }} pre {{ white-space: pre-wrap; background: white; color: black; border: 1px solid #aaa; }} }}
</style></head><body><header><h1>{title}</h1><p>Research draft | No benchmark results | Private review copy</p></header>
<div class="wrap"><aside aria-label="Document navigation"><strong>Contents</strong>{toc}</aside><main>{body}</main></div>
</body></html>"""
    (ROOT / "index.html").write_text(page, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    architecture()
    matrix()
    gate()
    build_html()
    print("Built three diagrams and the local review page.")
