#!/usr/bin/env python3
"""Build static task pages using summaries, without embedding source prompts."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
TASKS = json.loads((ROOT / 'data/tasks.json').read_text(encoding='utf-8'))
CONDITIONS = ('Baseline', 'Accessibility checklist', 'Prompt guidance', 'Skill', 'Validation agent', 'Combined')


def e(value):
    return html.escape(str(value), quote=True)


def page(title, description, main, prefix=''):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{e(description)}">
  <title>{e(title)} | AI accessibility study</title>
  <link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to main content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{prefix}index.html"><span aria-hidden="true">SPV</span>Accessibility study</a>
      <nav aria-label="Main navigation">
        <a href="{prefix}index.html#tasks">Tasks</a>
        <a href="{prefix}methodology.html">Methodology</a>
        <a href="{prefix}index.html#status">Study status</a>
      </nav>
    </div>
  </header>
  <main id="main">{main}</main>
  <footer><div class="wrap">AI website accessibility study &middot; Research in preparation</div></footer>
</body>
</html>
'''


def write(relative, text):
    target = DOCS / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8', newline='\n')


def render_home():
    cards = []
    for task in TASKS:
        cards.append(f'''<article class="card">
          <div class="card-top"><span class="number">{e(task['number'])} / 05</span><span class="category">{e(task['category'])}</span></div>
          <h3>{e(task['title'])}</h3>
          <p>{e(task['summary'])}</p>
          <p><span class="status">{e(task['status'])}</span></p>
          <a href="tasks/{e(task['slug'])}.html">View {e(task['title'].lower())} task</a>
        </article>''')
    main = '''
    <section class="hero wrap" aria-labelledby="hero-title">
      <div class="hero-layout">
        <div>
          <p class="eyebrow">Research in preparation</p>
          <h1 id="hero-title">Can AI build more accessible websites?</h1>
          <p class="lede">Five website requests will be used to study how accessibility guidance and verification influence AI-generated work.</p>
          <a class="button" href="#tasks">Explore the tasks</a>
        </div>
        <aside class="hero-note" aria-label="Study overview">
          <p><span class="status">Planning stage</span></p>
          <p><strong>Five selected tasks.</strong> A shared set of requests will be used across the comparison.</p>
          <p>Generated sites, test reports, and findings will appear here after they have been produced and reviewed.</p>
        </aside>
      </div>
    </section>
    <section id="tasks" class="section wrap" aria-labelledby="tasks-title">
      <div class="section-heading"><div><p class="eyebrow">The task set</p><h2 id="tasks-title">Five requests, five perspectives.</h2></div><p>Explore each task and its potential evaluation areas. The original prompt wording is kept separately.</p></div>
      <div class="grid">''' + '\n'.join(cards) + '''</div>
    </section>
    <section id="approach" class="section wrap" aria-labelledby="approach-title">
      <div class="section-heading"><div><p class="eyebrow">The approach</p><h2 id="approach-title">A comparison built on evidence.</h2></div><p>The study protocol and exact conditions are still being developed.</p></div>
      <div class="process">
        <div><p class="eyebrow">01 / Generate</p><h3>Use the same request</h3><p>Generate a separate site for each task and study condition.</p></div>
        <div><p class="eyebrow">02 / Evaluate</p><h3>Test the experience</h3><p>Use browser-based checks and human review of relevant interactions.</p></div>
        <div><p class="eyebrow">03 / Compare</p><h3>Report what happened</h3><p>Keep functionality, accessibility findings, and incomplete runs visible.</p></div>
      </div>
      <p><a href="methodology.html">Read the proposed methodology</a></p>
    </section>
    <section id="status" class="section wrap" aria-labelledby="status-title">
      <p class="eyebrow">Current status</p><h2 id="status-title">The study has not been run.</h2>
      <div class="notice"><p>The five task inputs are selected. The intervention packages, test plans, and analysis remain under discussion. This site does not report benchmark results.</p></div>
    </section>'''
    return page('Home', 'A study of accessibility in AI-generated websites.', main)


def render_task(task):
    checks = ''.join(f'<li>{e(item)}</li>' for item in task['possible_checks'])
    rows = ''.join(f'<tr><th scope="row">{e(name)}</th><td>Not run</td></tr>' for name in CONDITIONS)
    main = f'''
    <div class="wrap content">
      <p class="breadcrumb"><a href="../index.html#tasks">All tasks</a> / {e(task['number'])}</p>
      <p class="eyebrow">Task {e(task['number'])} / {e(task['category'])}</p>
      <h1>{e(task['title'])}</h1>
      <p class="lede">{e(task['summary'])}</p>
      <p><span class="status">{e(task['status'])}</span></p>
      <div class="notice"><p><strong>Current status:</strong> No generated site or evaluation result has been published for this task.</p></div>
      <h2>About the request</h2><p>{e(task['scope'])}</p>
      <p>The task is based on a selected first message in the <a href="https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k">WebDev Arena dataset</a>. This page summarizes its scope and does not reproduce the original prompt.</p>
      <h2>Possible checks</h2><p class="muted">These are ideas for the test plan, not completed tests or a finalized accessibility assessment.</p>
      <ul>{checks}</ul>
      <h2>Proposed conditions</h2><p>Conditions and their definitions remain under discussion.</p>
      <div class="table-wrap"><table><caption>Current task status by proposed condition</caption><thead><tr><th scope="col">Condition</th><th scope="col">Status</th></tr></thead><tbody>{rows}</tbody></table></div>
      <p><a href="../methodology.html">How the study is being designed</a></p>
    </div>'''
    return page(task['title'], task['summary'], main, prefix='../')


def render_methodology():
    main = '''
    <div class="wrap content">
      <p class="breadcrumb"><a href="index.html">Home</a> / Methodology</p>
      <p class="eyebrow">Working proposal</p>
      <h1>How the study is being designed.</h1>
      <p class="lede">The goal is to compare generated websites using the same tasks and clearly defined accessibility checks.</p>
      <div class="notice"><p><strong>Not yet finalized:</strong> Conditions, run counts, measurements, and analysis will be reviewed before the study begins.</p></div>
      <h2>Generate separate websites</h2>
      <p>The proposed comparison includes a baseline, a simple accessibility checklist, prompt guidance, a skill, a validation agent, and a combined configuration. The same task request would be used for every condition.</p>
      <h2>Evaluate behavior and accessibility</h2>
      <p>Proposed checks include task functionality, browser-based tests, and human review of keyboard use, focus, labels, and content. The exact checks depend on the task and the controls created.</p>
      <p>Automated checks detect some accessibility issues; they cannot establish complete accessibility or WCAG conformance. The <a href="https://www.w3.org/WAI/test-evaluate/tools/selecting/">W3C</a> and <a href="https://playwright.dev/docs/accessibility-testing">Playwright</a> describe these limitations.</p>
      <h2>Keep the evidence separate</h2>
      <p>Each attempted run should retain its configuration, generated artifact, test outcomes, and applicable limitations. Failed or incomplete runs should remain visible.</p>
      <h2>Research foundations</h2>
      <ul>
        <li><a href="https://doi.org/10.1145/3706598.3713335">CodeA11y, CHI 2025</a>: accessibility assistance for developers using AI coding tools.</li>
        <li><a href="https://doi.org/10.1145/3449287">Cognitive forcing functions, CSCW 2021</a>: an experiment on human decisions with AI assistance.</li>
        <li><a href="https://aclanthology.org/2025.findings-acl.1036/">ProjectEval, ACL Findings 2025</a>: project-level evaluation using simulated interactions.</li>
      </ul>
      <p>These studies inform the design. They do not establish the outcome of this study.</p>
    </div>'''
    return page('Methodology', 'The proposed method for evaluating generated websites.', main)


def main():
    if len(TASKS) != 5 or len({t['slug'] for t in TASKS}) != 5:
        raise ValueError('Expected five distinct task summaries.')
    write('index.html', render_home())
    write('methodology.html', render_methodology())
    for task in TASKS:
        write(f"tasks/{task['slug']}.html", render_task(task))
    print(f'Built 1 index, 1 methodology page, and {len(TASKS)} task pages.')


if __name__ == '__main__':
    main()
