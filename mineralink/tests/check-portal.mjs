import assert from 'node:assert/strict';
import {readFileSync, existsSync} from 'node:fs';
import {Script} from 'node:vm';
import {join, dirname} from 'node:path';

const root = join(process.cwd(), 'mineralink');
const read = file => readFileSync(join(root, file), 'utf8');
const portal = read('espace-client.html');
const home = read('index.html');
const gettingStarted = read('commencer.html');
const requiredIds = [
  'authForm','signup','orgForm','rfqForm','inviteForm',
  'inviteRfq','supplierId','quoteForm','rfqList','orgList','msg'
];
for (const id of requiredIds) assert.ok(portal.includes('id="' + id + '"'), 'Missing UI control: ' + id);
for (const op of [
  "db.auth.signUp", "db.auth.signInWithPassword", "register_organization",
  "submit_rfq", "invite_supplier", "from('quotes').insert", "from('quotes').select"
]) assert.ok(portal.includes(op), 'Missing flow operation: ' + op);
assert.ok(portal.includes('options:{emailRedirectTo:'), 'Email confirmation redirect is not in signUp options');
assert.ok(portal.includes('sb_publishable_'), 'Missing browser-safe publishable key');
assert.ok(!portal.includes('sb_secret_'), 'Secret API key must not be in public HTML');

const scriptMatch = portal.match(/<script type="module">([\s\S]*?)<\/script>/);
assert.ok(scriptMatch, 'Missing module script');
const moduleWithoutImport = scriptMatch[1].replace(/^\s*import\s+\{createClient\}[^;]*;\s*/, '');
new Script(moduleWithoutImport, {filename: 'espace-client.inline.js'});

for (const [name, html] of [['index.html', home], ['commencer.html', gettingStarted]]) {
  for (const [, href] of html.matchAll(/href="([^"]+)"/g)) {
    if (!href || /^(?:https?:|mailto:|tel:|#)/.test(href)) continue;
    const pagePath = href.split(/[?#]/)[0];
    assert.ok(existsSync(join(root, dirname(name), pagePath)), name + ' links to missing page: ' + pagePath);
  }
}
assert.ok(home.includes('href="espace-client.html"'), 'Homepage must link to portal');
assert.ok(gettingStarted.includes('href="espace-client.html"'), 'Getting-started page must link to portal');
console.log('MineraLink smoke checks passed: client JS, workflow, controls, internal links.');
