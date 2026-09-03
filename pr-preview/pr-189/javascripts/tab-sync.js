/*
 * Tab selection in the address bar (FR-053, FR-054).
 *
 * The reader's language choice travels in the page address as `?language=python` or
 * `?language=typescript`, so a link copied from the middle of the site opens in the same language
 * for whoever receives it. Every other tab axis the site grows -- operating system is the one this
 * file already declares -- gets its own parameter, and choosing a value on one axis never touches
 * another.
 *
 * WHAT MATERIAL ALREADY DOES, AND HOW THIS COOPERATES WITH IT
 *
 * Material for MkDocs 9.7.1 with `content.tabs.link` keeps its own memory of tab choices: on every
 * user switch it writes an array of label strings, most recent first, to localStorage under
 * `<base path>.__tabs` (`__md_set("__tabs", ...)` in
 * `material/templates/assets/javascripts/components/content/tabs/index.ts`), and an inline script
 * emitted by `partials/javascripts/content.html` reads it back and checks the matching input in
 * every `.tabbed-set` on the page. That script sits inside `[data-md-component=container]`, so
 * instant navigation re-executes it on every page swap.
 *
 * So the reconciliation is: the address wins when it carries a parameter, the stored preference is
 * the fallback when it does not. `docs/overrides/partials/tab-axes.html` promotes the address into
 * `__tabs` in the document head, which lets Material's own restore script do the DOM work before
 * the first paint. This file then re-applies the same decision against the DOM (belt and braces,
 * and the only path left when localStorage is unavailable) and stamps the address so the parameter
 * is there to be copied.
 *
 * WHY THIS RUNS ON `document$`
 *
 * `navigation.instant` swaps documents over XHR, so `DOMContentLoaded` fires once and never again.
 * Material exposes `window.document$` (a ReplaySubject of 1, assigned in `bundle.ts` and fed both
 * by `DOMContentLoaded` and by the instant-navigation injector), which is the documented hook for
 * "run after every document". `window.location$` fires for hash changes too and does not guarantee
 * the new document is in place, so it is the wrong subject here. Being a ReplaySubject, `document$`
 * is safe to subscribe to at any time. This file is loaded from `extra_javascript`, which lands at
 * the end of the body outside the swapped container, so it is evaluated exactly once.
 *
 * Instant navigation pushes the plain link href, which carries no query string, so re-stamping the
 * parameter after every navigation is what keeps the choice visible in the address.
 */
(function () {
  "use strict";

  /* Fallback registry, used only if `partials/tab-axes.html` is not installed. Keep in step. */
  var DEFAULT_AXES = [
    { param: "language", values: { python: "Python", typescript: "TypeScript" } },
    { param: "os", values: { macos: "macOS", linux: "Linux", windows: "Windows" } }
  ];

  var index = null;

  /** Normalise label text so matching survives whitespace and casing differences. */
  function normalize(text) {
    return String(text == null ? "" : text).replace(/\s+/g, " ").trim().toLowerCase();
  }

  /** Map of normalised label text -> { param, value }, built from the declared axes. */
  function labelIndex() {
    if (index) return index;
    var axes = window.__idfkitTabAxes;
    if (!Array.isArray(axes) || !axes.length) axes = DEFAULT_AXES;
    index = {};
    axes.forEach(function (axis) {
      Object.keys(axis.values || {}).forEach(function (value) {
        index[normalize(axis.values[value])] = { param: axis.param, value: value };
      });
    });
    return index;
  }

  /** The label paired with a tab input. Paired by id, never selected by it. */
  function labelFor(set, input) {
    var labels = set.querySelectorAll("label");
    for (var i = 0; i < labels.length; i++) {
      if (labels[i].htmlFor === input.id) return labels[i];
    }
    return null;
  }

  /**
   * One tab set, described by what its labels mean: `[{ input, value }]` plus the axis parameter
   * they belong to. A set whose labels match no declared axis reports `param: null` and is then
   * left completely alone -- "pip" / "uv" is not a language choice.
   */
  function describe(set) {
    var lookup = labelIndex();
    var inputs = set.querySelectorAll(":scope > input");
    var param = null;
    var options = [];
    for (var i = 0; i < inputs.length; i++) {
      var label = labelFor(set, inputs[i]);
      if (!label) continue;
      var hit = lookup[normalize(label.textContent)];
      if (!hit) continue;
      if (param === null) param = hit.param;
      if (hit.param !== param) continue;
      options.push({ input: inputs[i], value: hit.value });
    }
    return { param: param, options: options };
  }

  function storedLabels() {
    var stored = null;
    try {
      stored = typeof window.__md_get === "function" ? window.__md_get("__tabs") : null;
    } catch (e) {
      stored = null;
    }
    return Array.isArray(stored) ? stored : [];
  }

  function rememberLabels(labels) {
    if (!labels.length || typeof window.__md_set !== "function") return;
    var stored = storedLabels();
    var head = labels.filter(function (label, i) { return labels.indexOf(label) === i; });
    var next = head.concat(stored.filter(function (tab) { return head.indexOf(tab) < 0; }));
    if (next.length === stored.length && next.every(function (tab, i) { return tab === stored[i]; })) return;
    try {
      window.__md_set("__tabs", next);
    } catch (e) {
      /* storage unavailable; the address still carries the choice */
    }
  }

  /** The stored preference for one axis, as a value, or null. */
  function storedValue(param) {
    var lookup = labelIndex();
    var stored = storedLabels();
    for (var i = 0; i < stored.length; i++) {
      var hit = lookup[normalize(stored[i])];
      if (hit && hit.param === param) return hit.value;
    }
    return null;
  }

  /** Canonical label for a value, for writing back into Material's store. */
  function labelOf(param, value) {
    var axes = window.__idfkitTabAxes;
    if (!Array.isArray(axes) || !axes.length) axes = DEFAULT_AXES;
    for (var i = 0; i < axes.length; i++) {
      if (axes[i].param === param) return (axes[i].values || {})[value] || null;
    }
    return null;
  }

  /**
   * Rewrite the address in place. `replaceState`, never `pushState`: one history entry per tab
   * click would make the back button useless. `history.state` is carried over because Material
   * keeps its scroll-restoration offset there.
   */
  function replace(url) {
    var next = url.pathname + url.search + url.hash;
    if (next === location.pathname + location.search + location.hash) return;
    try {
      history.replaceState(history.state, "", next);
    } catch (e) {
      /* `file:` origins and the like; the tabs are still correct on the page */
    }
  }

  /**
   * Reconcile address, stored preference and DOM for every axis present on this page, then stamp
   * the address. Axes with no tab set on the page are not stamped, and parameters already in the
   * address are left untouched, so a page with no tabs at all is a no-op.
   */
  function sync() {
    var sets = document.querySelectorAll(".tabbed-set");
    if (!sets.length) return;

    var groups = {};
    for (var i = 0; i < sets.length; i++) {
      var described = describe(sets[i]);
      if (!described.param) continue;
      (groups[described.param] = groups[described.param] || []).push(described);
    }

    var params = Object.keys(groups);
    if (!params.length) return;

    var url = new URL(location.href);
    var chosenLabels = [];

    params.forEach(function (param) {
      var group = groups[param];
      var offered = {};
      var firstValue = null;
      var checkedValue = null;
      group.forEach(function (described) {
        described.options.forEach(function (option) {
          offered[option.value] = true;
          if (firstValue === null) firstValue = option.value;
          if (checkedValue === null && option.input.checked) checkedValue = option.value;
        });
      });
      var fallback = checkedValue || firstValue;

      /* The address is the source of truth when it names a value this page actually offers. */
      var requested = url.searchParams.get(param);
      var value = requested && offered[normalize(requested)] ? normalize(requested) : null;

      /* Otherwise the stored preference, even when this page does not offer it: the reader's
         choice is not downgraded by a page that happens to show only one side. */
      if (!value) value = storedValue(param);
      if (!value) value = fallback;
      if (!value) return;

      group.forEach(function (described) {
        described.options.forEach(function (option) {
          if (option.value === value && !option.input.checked) option.input.checked = true;
        });
      });

      url.searchParams.set(param, value);
      var label = labelOf(param, value);
      if (label) chosenLabels.push(label);
    });

    rememberLabels(chosenLabels);
    replace(url);
  }

  /**
   * A reader switching a tab rewrites that axis's parameter and nothing else. Material's own
   * linking clicks the matching tab in every other set, which lands here again with the same
   * label and the same value, so the extra events are idempotent.
   */
  document.addEventListener("change", function (ev) {
    var input = ev.target;
    if (!input || input.tagName !== "INPUT" || !input.checked) return;
    var set = input.closest ? input.closest(".tabbed-set") : null;
    if (!set) return;
    var label = labelFor(set, input);
    if (!label) return;
    var hit = labelIndex()[normalize(label.textContent)];
    if (!hit) return;
    var url = new URL(location.href);
    if (url.searchParams.get(hit.param) === hit.value) return;
    url.searchParams.set(hit.param, hit.value);
    replace(url);
  });

  /* Once now, since this script is evaluated after the tab markup, and once after every instant
     navigation. Running twice on first load is harmless: `sync` is idempotent. */
  sync();
  var document$ = window.document$;
  if (document$ && typeof document$.subscribe === "function") {
    document$.subscribe(function () { sync(); });
  } else {
    document.addEventListener("DOMContentLoaded", sync);
  }
})();
