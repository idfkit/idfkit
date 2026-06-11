/* idfkit tmy browser — client-side map + filter + download */

(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const MAX_LIST = 100;
  const MOBILE_BREAKPOINT = 768;

  let allStations = [];
  let allGroups = [];
  let filteredGroups = [];
  let map = null;
  let clusterGroup = null;
  let canvasRenderer = null;
  const markerByGroup = new Map();
  let config = null;
  let baseLayer = null;
  const darkMedia = window.matchMedia('(prefers-color-scheme: dark)');

  /* ── Utilities ─────────────────────────────────────────── */

  const displayName = (s) => {
    const name = (s.city || '').replace(/\./g, ' ').replace(/-/g, ' ').trim();
    const parts = [];
    if (name) parts.push(name);
    if (s.state) parts.push(s.state);
    if (s.country) parts.push(s.country);
    return parts.join(', ');
  };

  const datasetVariant = (s) => {
    const file = (s.url || '').split('/').pop() || '';
    const stem = file.replace(/\.zip$/i, '');
    const idx = stem.lastIndexOf('_');
    return idx >= 0 ? stem.slice(idx + 1) : stem;
  };

  const filenameStem = (s) => {
    const file = (s.url || '').split('/').pop() || '';
    return file.replace(/\.zip$/i, '');
  };

  const haversineKm = (lat1, lon1, lat2, lon2) => {
    const R = 6371;
    const toRad = (d) => (d * Math.PI) / 180;
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a =
      Math.sin(dLat / 2) ** 2 +
      Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(a));
  };

  // Read a number input. Returns null when blank or NaN so callers can
  // distinguish "no constraint" from "0".
  const numOrNull = (id) => {
    const v = $(id).value;
    if (v === '' || v == null) return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  };

  // ASHRAE labels look like "4A - Mixed - Humid". The first whitespace-
  // separated token is the canonical zone code we sort and group by.
  const zoneCode = (label) => (label || '').split(/\s+/)[0] || '';

  const toast = (msg, variant = '') => {
    const el = $('toast');
    el.textContent = msg;
    el.className = 'visible ' + variant;
    clearTimeout(el._t);
    el._t = setTimeout(() => {
      el.className = '';
    }, 3000);
  };

  /* ── Loading ───────────────────────────────────────────── */

  async function loadStations() {
    const resp = await fetch('stations.json.gz');
    if (!resp.ok) throw new Error(`stations fetch failed: ${resp.status}`);
    const buf = await resp.arrayBuffer();
    const bytes = new Uint8Array(buf);
    let text;
    // If the server set Content-Encoding: gzip (Python http.server
    // mode), the browser already decompressed and `bytes` is plain
    // JSON. Otherwise (static CDN serving the .json.gz as a raw
    // file), we see the gzip magic 0x1f 0x8b and decompress here.
    if (bytes.length >= 2 && bytes[0] === 0x1f && bytes[1] === 0x8b) {
      if (!('DecompressionStream' in window)) {
        throw new Error('Browser lacks DecompressionStream — use a recent Chrome/Firefox/Safari');
      }
      const stream = new Blob([buf]).stream().pipeThrough(new DecompressionStream('gzip'));
      text = await new Response(stream).text();
    } else {
      text = new TextDecoder().decode(bytes);
    }
    const data = JSON.parse(text);
    return data.stations || [];
  }

  // Relative paths so the app works both when served by the Python
  // http.server (base = "/") and when embedded as static assets under
  // a subpath (e.g. mkdocs site at /weather/browse/).
  let staticMode = false;

  async function loadConfig() {
    // Opt-in flag for static deploys — avoids a spurious 404 in the
    // devtools console when there is no Python server behind the page.
    const params = new URLSearchParams(window.location.search);
    if (params.has('static')) {
      staticMode = true;
      return {};
    }
    try {
      const resp = await fetch('api/config');
      if (resp.ok) return resp.json();
    } catch {
      // fall through to static-mode fallback
    }
    staticMode = true;
    return {};
  }

  /* ── Grouping ──────────────────────────────────────────── */

  /** Group stations by WMO (fallback: filename stem). A single group
   *  represents one physical weather station with N dataset variants. */
  function groupStations(stations) {
    const groups = new Map();
    for (const s of stations) {
      const key = (s.wmo && s.wmo.trim()) || filenameStem(s);
      let g = groups.get(key);
      if (!g) {
        g = {
          key,
          wmo: s.wmo,
          country: s.country,
          state: s.state,
          city: s.city,
          latitude: s.latitude,
          longitude: s.longitude,
          elevation: s.elevation,
          timezone: s.timezone,
          ashrae_climate_zone: s.ashrae_climate_zone || '',
          heating_design_db_c: s.heating_design_db_c,
          cooling_design_db_c: s.cooling_design_db_c,
          hdd18: s.hdd18,
          cdd10: s.cdd10,
          design_conditions_source_wmo: s.design_conditions_source_wmo || null,
          variants: [],
        };
        groups.set(key, g);
      }
      g.variants.push(s);
    }

    // Sort variants within each group so the default "TMYx" (no year range)
    // shows first, then year-range variants newest-first.
    for (const g of groups.values()) {
      g.variants.sort((a, b) => {
        const va = datasetVariant(a);
        const vb = datasetVariant(b);
        const ya = /(\d{4})-(\d{4})$/.exec(va);
        const yb = /(\d{4})-(\d{4})$/.exec(vb);
        if (!ya && yb) return -1;
        if (ya && !yb) return 1;
        if (ya && yb) return Number(yb[2]) - Number(ya[2]);
        return va.localeCompare(vb);
      });
    }

    return Array.from(groups.values());
  }

  /* ── Filtering ─────────────────────────────────────────── */

  function applyFilters() {
    const q = ($('search').value || '').trim().toLowerCase();
    const country = ($('country').value || '').trim().toUpperCase();
    const state = ($('state').value || '').trim().toUpperCase();
    const variantQ = ($('variant').value || '').trim().toLowerCase();
    const zone = $('climate-zone').value || '';
    const elevMin = numOrNull('elev-min');
    const elevMax = numOrNull('elev-max');
    const heatMin = numOrNull('heat-min');
    const heatMax = numOrNull('heat-max');
    const coolMin = numOrNull('cool-min');
    const coolMax = numOrNull('cool-max');
    const hddMin = numOrNull('hdd-min');
    const hddMax = numOrNull('hdd-max');
    const cddMin = numOrNull('cdd-min');
    const cddMax = numOrNull('cdd-max');
    const qTokens = q ? q.split(/\s+/).filter(Boolean) : [];

    let out = [];
    for (const g of allGroups) {
      if (country && g.country.toUpperCase() !== country) continue;
      if (state && g.state.toUpperCase() !== state) continue;
      if (zone && zoneCode(g.ashrae_climate_zone) !== zone) continue;
      if (elevMin != null && g.elevation < elevMin) continue;
      if (elevMax != null && g.elevation > elevMax) continue;
      if (heatMin != null && g.heating_design_db_c < heatMin) continue;
      if (heatMax != null && g.heating_design_db_c > heatMax) continue;
      if (coolMin != null && g.cooling_design_db_c < coolMin) continue;
      if (coolMax != null && g.cooling_design_db_c > coolMax) continue;
      if (hddMin != null && g.hdd18 < hddMin) continue;
      if (hddMax != null && g.hdd18 > hddMax) continue;
      if (cddMin != null && g.cdd10 < cddMin) continue;
      if (cddMax != null && g.cdd10 > cddMax) continue;
      if (variantQ && !g.variants.some((v) => datasetVariant(v).toLowerCase().includes(variantQ))) {
        continue;
      }
      if (qTokens.length) {
        const hay = (
          displayName(g) +
          ' ' +
          (g.wmo || '') +
          ' ' +
          g.variants.map(filenameStem).join(' ')
        ).toLowerCase();
        if (!qTokens.every((t) => hay.includes(t))) continue;
      }
      out.push(g);
    }

    // Spatial ordering when config seeded a map center
    if (config && config.lat != null && config.lon != null) {
      out = out
        .map((g) => ({ g, d: haversineKm(config.lat, config.lon, g.latitude, g.longitude) }))
        .filter((x) => config.max_km == null || x.d <= config.max_km)
        .sort((a, b) => a.d - b.d)
        .map((x) => x.g);
    }

    filteredGroups = out;
    renderResults();
    renderMarkers();
  }

  /* ── Rendering ─────────────────────────────────────────── */

  function renderResults() {
    const list = $('results');
    const totalGroups = filteredGroups.length;
    const totalVariants = filteredGroups.reduce((n, g) => n + g.variants.length, 0);
    $('total').textContent = totalGroups.toLocaleString();
    $('total-variants').textContent = totalVariants.toLocaleString();

    list.innerHTML = '';
    const shown = filteredGroups.slice(0, MAX_LIST);
    const frag = document.createDocumentFragment();

    for (const g of shown) {
      const row = document.createElement('div');
      row.className = 'result';

      const name = document.createElement('div');
      name.className = 'name';
      name.textContent = displayName(g);
      row.appendChild(name);

      const meta = document.createElement('div');
      meta.className = 'meta';

      if (g.wmo) {
        const wmo = document.createElement('span');
        wmo.className = 'wmo';
        wmo.textContent = 'WMO ' + g.wmo;
        meta.appendChild(wmo);
      }

      const count = document.createElement('span');
      count.className = 'count';
      count.textContent = g.variants.length + (g.variants.length === 1 ? ' dataset' : ' datasets');
      meta.appendChild(count);

      const zc = zoneCode(g.ashrae_climate_zone);
      if (zc) {
        const zone = document.createElement('span');
        zone.className = 'zone';
        zone.textContent = zc;
        meta.appendChild(zone);
      }

      if (config && config.lat != null && config.lon != null) {
        const d = haversineKm(config.lat, config.lon, g.latitude, g.longitude);
        const dist = document.createElement('span');
        dist.className = 'dist';
        dist.textContent = d.toFixed(0) + ' km';
        meta.appendChild(dist);
      }

      row.appendChild(meta);
      row.addEventListener('click', () => focusGroup(g));
      frag.appendChild(row);
    }

    if (totalGroups > MAX_LIST) {
      const more = document.createElement('div');
      more.className = 'result muted small';
      more.textContent = `+ ${totalGroups - MAX_LIST} more — refine filters to narrow`;
      frag.appendChild(more);
    }

    if (totalGroups === 0) {
      const empty = document.createElement('div');
      empty.className = 'result muted';
      empty.textContent = 'No stations match.';
      frag.appendChild(empty);
    }

    list.appendChild(frag);
  }

  function currentMarkerStyle() {
    const cs = getComputedStyle(document.documentElement);
    const accent = cs.getPropertyValue('--accent').trim() || '#3ea6ff';
    return {
      renderer: canvasRenderer,
      radius: 5,
      weight: 1,
      color: '#ffffff',
      fillColor: accent,
      fillOpacity: 0.85,
      opacity: 1,
    };
  }

  function renderMarkers() {
    if (!clusterGroup) return;
    clusterGroup.clearLayers();
    markerByGroup.clear();

    // Canvas-rendered circle markers: one <canvas> paints all 17k dots,
    // so Safari/Chrome only recomposite a single layer on zoom/pan.
    const style = currentMarkerStyle();
    const markers = [];
    for (const g of filteredGroups) {
      const m = L.circleMarker([g.latitude, g.longitude], style);
      m._tmyGroup = g;
      markers.push(m);
      markerByGroup.set(g, m);
    }
    clusterGroup.addLayers(markers);
  }

  function retintMarkers() {
    if (!clusterGroup || markerByGroup.size === 0) return;
    const { fillColor } = currentMarkerStyle();
    clusterGroup.eachLayer((layer) => {
      if (typeof layer.setStyle === 'function') layer.setStyle({ fillColor });
    });
  }

  /* ── Focus / detail ────────────────────────────────────── */

  function focusGroup(g) {
    // On mobile, a click on a result row needs to surface the map
    // before the dialog opens — otherwise the cluster zoom animation
    // runs against a hidden pane and the user lands on a blank screen
    // when they close the dialog.
    if (isMobile()) setView('map');
    map.setView([g.latitude, g.longitude], Math.max(map.getZoom(), 8));
    const m = markerByGroup.get(g);
    if (m && clusterGroup.hasLayer(m)) {
      clusterGroup.zoomToShowLayer(m, () => openDetail(g));
    } else {
      openDetail(g);
    }
  }

  const fmtTemp = (c) =>
    c == null || !Number.isFinite(c) ? '—' : `${c.toFixed(1)} °C / ${(c * 9 / 5 + 32).toFixed(1)} °F`;
  const fmtInt = (n) => (n == null || !Number.isFinite(n) ? '—' : n.toLocaleString());

  function openDetail(g) {
    $('detail-name').textContent = displayName(g);
    $('detail-wmo').textContent = g.wmo || '—';
    $('detail-country').textContent = g.country || '—';
    $('detail-state').textContent = g.state || '—';
    $('detail-coords').textContent = `${g.latitude.toFixed(4)}, ${g.longitude.toFixed(4)}`;
    $('detail-elev').textContent = `${g.elevation} m`;
    $('detail-tz').textContent = `GMT ${g.timezone >= 0 ? '+' : ''}${g.timezone}`;
    $('detail-zone').textContent = g.ashrae_climate_zone || '—';
    $('detail-heat').textContent = fmtTemp(g.heating_design_db_c);
    $('detail-cool').textContent = fmtTemp(g.cooling_design_db_c);
    $('detail-hdd').textContent = fmtInt(g.hdd18);
    $('detail-cdd').textContent = fmtInt(g.cdd10);

    const list = $('variant-list');
    list.innerHTML = '';
    for (const v of g.variants) {
      list.appendChild(renderVariantRow(v));
    }

    const dlg = $('detail');
    if (typeof dlg.showModal === 'function') dlg.showModal();
    else dlg.setAttribute('open', '');
  }

  function renderVariantRow(v) {
    const li = document.createElement('li');
    li.className = 'variant-row';

    const info = document.createElement('div');
    info.className = 'variant-info';
    const name = document.createElement('div');
    name.className = 'variant-name';
    name.textContent = datasetVariant(v);
    info.appendChild(name);
    const sub = document.createElement('div');
    sub.className = 'variant-sub muted small';
    sub.textContent = v.source || '';
    info.appendChild(sub);
    li.appendChild(info);

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'variant-download';
    btn.textContent = 'Download .zip';
    btn.addEventListener('click', () => triggerDownload(v, btn));
    li.appendChild(btn);

    return li;
  }

  async function triggerDownload(s, btn) {
    const original = btn.textContent;

    // Static-mode (no Python server): open the upstream ZIP in a new tab.
    // Bypasses idfkit's shared cache but keeps the UI usable when embedded
    // as read-only docs.
    if (staticMode) {
      window.open(s.url, '_blank', 'noopener,noreferrer');
      btn.textContent = 'Opened ↗';
      toast(`Opened ${filenameStem(s)}.zip on climate.onebuilding.org`, 'good');
      setTimeout(() => {
        btn.textContent = original;
      }, 2500);
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Fetching…';

    const stem = filenameStem(s);
    const url =
      'api/zip?wmo=' +
      encodeURIComponent(s.wmo || '') +
      '&filename=' +
      encodeURIComponent(stem);

    let objectUrl = null;
    try {
      const resp = await fetch(url);
      if (!resp.ok) {
        const msg = await resp.text();
        throw new Error(msg || `download failed (${resp.status})`);
      }
      const blob = await resp.blob();
      objectUrl = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = objectUrl;
      a.download = stem + '.zip';
      document.body.appendChild(a);
      a.click();
      a.remove();

      btn.textContent = 'Saved ✓';
      btn.disabled = false;
      toast(`Saved ${stem}.zip`, 'good');
      setTimeout(() => {
        btn.textContent = original;
      }, 2500);
    } catch (err) {
      btn.disabled = false;
      btn.textContent = 'Retry';
      toast(err.message || String(err), 'bad');
    } finally {
      if (objectUrl) setTimeout(() => URL.revokeObjectURL(objectUrl), 10000);
    }
  }

  /* ── Initialisation ────────────────────────────────────── */

  function tileLayerForScheme() {
    const variant = darkMedia.matches ? 'dark_all' : 'light_all';
    return L.tileLayer(
      `https://{s}.basemaps.cartocdn.com/${variant}/{z}/{x}/{y}{r}.png`,
      {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> ' +
          '&copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19,
      },
    );
  }

  function applyColorScheme() {
    if (!map) return;
    if (baseLayer) map.removeLayer(baseLayer);
    baseLayer = tileLayerForScheme().addTo(map);
    retintMarkers();
  }

  function initMap() {
    map = L.map('map', {
      center: [30, 0],
      zoom: 2,
      worldCopyJump: true,
      preferCanvas: true,
    });
    // Single canvas renderer shared by every circleMarker on the map:
    // painting happens in one <canvas>, not 17k DOM nodes.
    canvasRenderer = L.canvas({ padding: 0.5 });

    applyColorScheme();
    darkMedia.addEventListener('change', applyColorScheme);

    clusterGroup = L.markerClusterGroup({
      chunkedLoading: true,
      chunkInterval: 120,
      maxClusterRadius: 80,
      disableClusteringAtZoom: 12,
      spiderfyOnMaxZoom: false,
      showCoverageOnHover: false,
      zoomToBoundsOnClick: true,
      animate: true,
      animateAddingMarkers: false,
    });

    // One delegated click handler for all 17k markers.
    clusterGroup.on('click', (e) => {
      const group = e.layer && e.layer._tmyGroup;
      if (group) openDetail(group);
    });

    map.addLayer(clusterGroup);
  }

  function seedFiltersFromConfig(cfg) {
    if (!cfg) return;
    if (cfg.query) $('search').value = cfg.query;
    if (cfg.country) $('country').value = cfg.country;
    if (cfg.state) $('state').value = cfg.state;
    if (cfg.variant) $('variant').value = cfg.variant;
  }

  function populateClimateZoneOptions(groups) {
    const select = $('climate-zone');
    const seen = new Map(); // code -> full label
    for (const g of groups) {
      const code = zoneCode(g.ashrae_climate_zone);
      if (!code) continue;
      if (!seen.has(code)) seen.set(code, g.ashrae_climate_zone);
    }
    const codes = Array.from(seen.keys()).sort((a, b) =>
      a.localeCompare(b, undefined, { numeric: true }),
    );
    const frag = document.createDocumentFragment();
    for (const c of codes) {
      const opt = document.createElement('option');
      opt.value = c;
      opt.textContent = seen.get(c);
      frag.appendChild(opt);
    }
    select.appendChild(frag);
  }

  function resetFilters() {
    const ids = [
      'search', 'country', 'state', 'variant',
      'elev-min', 'elev-max',
      'heat-min', 'heat-max',
      'cool-min', 'cool-max',
      'hdd-min', 'hdd-max',
      'cdd-min', 'cdd-max',
    ];
    for (const id of ids) $(id).value = '';
    $('climate-zone').value = '';
    applyFilters();
  }

  /* ── View toggle (mobile) ───────────────────────────────── */

  const isMobile = () => window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT}px)`).matches;

  function setView(view) {
    const body = document.body;
    body.classList.remove('view-list', 'view-map');
    body.classList.add(view === 'map' ? 'view-map' : 'view-list');
    for (const btn of document.querySelectorAll('#mobile-bar .view-toggle button')) {
      btn.setAttribute('aria-selected', btn.dataset.view === view ? 'true' : 'false');
    }
    // Leaflet caches its container size; re-measure when the map pane
    // becomes visible so tiles fill the new viewport correctly.
    if (view === 'map' && map) {
      requestAnimationFrame(() => map.invalidateSize());
    }
  }

  function wireInputs() {
    const debounce = (fn, ms) => {
      let t;
      return (...args) => {
        clearTimeout(t);
        t = setTimeout(() => fn(...args), ms);
      };
    };
    const handler = debounce(applyFilters, 150);
    const filterIds = [
      'search', 'country', 'state', 'variant',
      'elev-min', 'elev-max',
      'heat-min', 'heat-max',
      'cool-min', 'cool-max',
      'hdd-min', 'hdd-max',
      'cdd-min', 'cdd-max',
    ];
    for (const id of filterIds) $(id).addEventListener('input', handler);
    $('climate-zone').addEventListener('change', applyFilters);
    $('reset-filters').addEventListener('click', resetFilters);

    for (const btn of document.querySelectorAll('#mobile-bar .view-toggle button')) {
      btn.addEventListener('click', () => setView(btn.dataset.view));
    }

    $('detail-close').addEventListener('click', () => $('detail').close());
    $('detail').addEventListener('click', (e) => {
      if (e.target.id === 'detail') $('detail').close();
    });
  }

  async function boot() {
    initMap();
    wireInputs();

    try {
      toast('Loading station index…');
      const [stations, cfg] = await Promise.all([loadStations(), loadConfig()]);
      allStations = stations;
      allGroups = groupStations(stations);
      config = cfg;
      seedFiltersFromConfig(cfg);
      populateClimateZoneOptions(allGroups);

      if (cfg && cfg.lat != null && cfg.lon != null) {
        map.setView([cfg.lat, cfg.lon], 6);
      }

      applyFilters();
      toast(
        `Loaded ${allGroups.length.toLocaleString()} stations (${allStations.length.toLocaleString()} datasets)`,
        'good',
      );
    } catch (err) {
      console.error(err);
      toast('Failed to load stations: ' + (err.message || err), 'bad');
    }
  }

  document.addEventListener('DOMContentLoaded', boot);
})();
