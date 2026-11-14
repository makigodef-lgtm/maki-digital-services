import assert from 'node:assert/strict';
import {readFileSync, existsSync} from 'node:fs';
import {Script} from 'node:vm';
import {join, dirname} from 'node:path';

const root = join(process.cwd(), 'mineralink');
const read = file => readFileSync(join(root, file), 'utf8');
const portal = read('espace-client.html');
const home = read('index.html');
const gettingStarted = read('commencer.html');
const privacy = read('confidentialite.html');
const terms = read('conditions-utilisation.html');
const installer = read('installer.html');
const worker = read('sw.js');
const manifest = JSON.parse(read('manifest.webmanifest'));
assert.ok(manifest.display === 'standalone', 'Installable PWA must use standalone display');
assert.ok(manifest.start_url === './' && manifest.scope === './', 'PWA scope should remain within MineraLink');
assert.ok(manifest.icons.some(x => x.sizes === '192x192'), 'Missing 192px app icon declaration');
assert.ok(manifest.icons.some(x => x.sizes === '512x512'), 'Missing 512px app icon declaration');
assert.ok(portal.includes('rel="manifest"'), 'Client portal missing install manifest');
assert.ok(portal.includes('id="signupConsent"'), 'New users must be informed about privacy and terms');
assert.ok(privacy.includes('Supabase Auth') && privacy.includes('demandes de devis'), 'Privacy notice must cover active client data');
assert.ok(terms.includes('MineraLink RDC'), 'Missing service conditions');
assert.ok(installer.includes('Windows, macOS ou Linux') && installer.includes('iPhone et iPad'), 'Device installation guides incomplete');
assert.ok(worker.includes("url.pathname.endsWith('/espace-client.html')"), 'Private account pages must not be cached by service worker');

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

for (const [name, html] of [['index.html', home], ['commencer.html', gettingStarted], ['espace-client.html', portal], ['installer.html', installer], ['confidentialite.html', privacy], ['conditions-utilisation.html', terms]]) {
  for (const [, href] of html.matchAll(/href="([^"]+)"/g)) {
    if (!href || /^(?:https?:|mailto:|tel:|#)/.test(href)) continue;
    const pagePath = href.split(/[?#]/)[0];
    if (['assets/icon-192.png','assets/icon-512.png'].includes(pagePath)) {
      assert.ok(existsSync(join(root, 'generate_icons.py')), 'PWA PNG icon generator missing');
      continue;
    }
    assert.ok(existsSync(join(root, dirname(name), pagePath)), name + ' links to missing page: ' + pagePath);
  }
}
assert.ok(home.includes('href="espace-client.html"'), 'Homepage must link to portal');
assert.ok(gettingStarted.includes('href="espace-client.html"'), 'Getting-started page must link to portal');
console.log('MineraLink smoke checks passed: PWA, client JS, workflow, privacy, terms, installability, internal links.');
