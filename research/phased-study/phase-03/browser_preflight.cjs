#!/usr/bin/env node
'use strict';

const path = require('node:path');
const { createRequire } = require('node:module');

async function main() {
  const [pilotDir, rawUrl] = process.argv.slice(2);
  if (!pilotDir || !rawUrl || process.argv.length !== 4) {
    throw new Error('Usage: node browser_preflight.cjs PILOT_DIR LOOPBACK_URL');
  }
  const target = new URL(rawUrl);
  if (!['http:', 'https:'].includes(target.protocol) ||
      !['localhost', '127.0.0.1', '[::1]'].includes(target.hostname) ||
      target.username || target.password) {
    throw new Error('Target must be a loopback HTTP(S) URL without credentials.');
  }
  const pilotRequire = createRequire(path.resolve(pilotDir, 'package.json'));
  const { chromium } = pilotRequire('playwright');
  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext({ serviceWorkers: 'block', viewport: { width: 1280, height: 720 } });
    let blocked = 0;
    let pageErrors = 0;
    let failedRequests = 0;
    await context.route('**/*', async route => {
      const request = route.request();
      const url = new URL(request.url());
      if (url.origin === target.origin && ['GET', 'HEAD'].includes(request.method())) {
        return route.continue();
      }
      blocked += 1;
      return route.abort();
    });
    const page = await context.newPage();
    page.on('pageerror', () => { pageErrors += 1; });
    page.on('requestfailed', () => { failedRequests += 1; });
    const response = await page.goto(target.href, { waitUntil: 'load', timeout: 30000 });
    if (!response || !response.ok() || new URL(page.url()).origin !== target.origin) {
      throw new Error('Navigation failed or moved outside the target origin.');
    }
    const text = (await page.locator('body').innerText()).trim();
    console.log(JSON.stringify({
      status: text.length ? 'visible_text_observed' : 'blank_initial_state',
      visible_text_characters: text.length,
      page_errors: pageErrors,
      failed_requests: failedRequests,
      blocked_requests: blocked,
      browser_version: browser.version(),
      limitation: 'Visible text does not prove the site rendered completely or that a journey works.'
    }));
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error.message);
  process.exitCode = 1;
});
