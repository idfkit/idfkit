/*
 * The reader-initiated browser-simulation runner (FR-072, SC-027, SC-029).
 *
 * WHAT IT IS, AND THE ONE RULE IT OBEYS
 *
 * A button on the browser-simulation how-to that, when a reader presses it, downloads
 * `@idfkit/engine` and about 51 MB of `@idfkit/engine-assets` from a CDN and runs EnergyPlus in
 * their tab. The rule is that NOTHING above happens before the press. No preload, no prefetch
 * hint, no import at parse time, no size probe. A documentation page that quietly pulls 51 MB
 * because somebody scrolled past it is a documentation page nobody on a metered connection can
 * read, and the site's own CI asserts that the built site hosts no engine bytes at all.
 *
 * WHY IT EXECUTES A FILE RATHER THAN CODE WRITTEN HERE
 *
 * It fetches `snippets/js/how-to/run-a-simulation-in-the-browser/live_runner.js` from this site,
 * which is the same file `npm run typecheck:docs` compiles in idfkit-js, and evaluates it as a
 * module. One rewrite happens on the way: bare specifiers become CDN URLs, because a browser
 * cannot resolve `@idfkit/core` on its own. Nothing else is transformed, which is why that file
 * is JavaScript with JSDoc types rather than TypeScript. A widget that ran a paraphrase of the
 * example it displays would be worse than no widget: it would look like evidence and be none.
 *
 * WHAT IT DOES NOT ESTABLISH
 *
 * That the example is correct. Nothing in CI runs EnergyPlus in a browser (research, Known
 * gaps). The type-check is what catches a renamed engine API; this is a demonstration a reader
 * can operate for themselves, and the page says so.
 *
 * DEGRADING (SC-029)
 *
 * Every failure path ends in the same place: the example stays on the page as text, and the
 * status line says what could not be reached. A reader offline, behind a proxy that blocks the
 * CDN, or on a browser without WebAssembly loses the button and nothing else.
 */

(() => {
  'use strict';

  /* jsDelivr serves the published packages as ES modules. Versions are pinned: an unpinned
     specifier would silently start executing a different EnergyPlus release than the page says
     it does, which is exactly the claim FR-073 asks the page to make precisely. */
  const ENGINE = 'https://cdn.jsdelivr.net/npm/@idfkit/engine@0.3.0/+esm';
  const CORE = 'https://cdn.jsdelivr.net/npm/@idfkit/core@0.1.0/+esm';
  const SCHEMAS = 'https://cdn.jsdelivr.net/npm/@idfkit/schemas@0.1.0/+esm';
  const ASSETS = 'https://cdn.jsdelivr.net/npm/@idfkit/engine-assets@26.1';

  const SPECIFIERS = new Map([
    ['@idfkit/engine', ENGINE],
    ['@idfkit/core', CORE],
    ['@idfkit/schemas', SCHEMAS],
  ]);

  /** The checked example, rewritten only so a browser can resolve its imports. */
  function withResolvableImports(source) {
    let rewritten = source;
    for (const [bare, url] of SPECIFIERS) {
      rewritten = rewritten.split(`'${bare}'`).join(`'${url}'`);
    }
    return rewritten;
  }

  function moduleUrl(source) {
    return URL.createObjectURL(new Blob([source], { type: 'text/javascript' }));
  }

  async function activate(root) {
    const status = root.querySelector('[data-engine-status]');
    const button = root.querySelector('[data-engine-run]');
    const say = (message) => {
      status.textContent = message;
    };

    button.disabled = true;
    let objectUrl;
    try {
      say('Fetching the example…');
      const response = await fetch(root.dataset.engineExample);
      if (!response.ok) throw new Error(`the example returned HTTP ${response.status}`);
      const source = await response.text();

      say('Downloading the engine and its assets. This is about 51 MB and happens once.');
      objectUrl = moduleUrl(withResolvableImports(source));
      const example = await import(/* webpackIgnore: true */ objectUrl);

      const { SchemaBundle, httpSource } = await import(/* webpackIgnore: true */ CORE);
      const schema = await new SchemaBundle(httpSource(root.dataset.engineSchemas)).load('26.1.0');

      const epw = await fetch(root.dataset.engineWeather).then((r) => r.text());
      await example.run(schema, epw, ASSETS, say);
    } catch (error) {
      /* SC-029: the example is already on the page as text and stays there. */
      say(
        `Could not run it here: ${error && error.message ? error.message : error}. ` +
          'The example above is the whole of it; copy it into a project instead.'
      );
    } finally {
      if (objectUrl) URL.revokeObjectURL(objectUrl);
      button.disabled = false;
    }
  }

  function attach() {
    for (const root of document.querySelectorAll('[data-engine-example]')) {
      if (root.dataset.engineAttached) continue;
      root.dataset.engineAttached = '1';
      const button = root.querySelector('[data-engine-run]');
      if (button) button.addEventListener('click', () => void activate(root));
    }
  }

  /* document$ is Material's per-navigation hook, so the button survives instant navigation.
     Falling back to a plain listener keeps this working if that ever goes away. */
  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(attach);
  } else {
    document.addEventListener('DOMContentLoaded', attach);
  }
})();
