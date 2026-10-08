import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { runInNewContext } from "node:vm";

const html = await readFile(new URL("../site/index.html", import.meta.url), "utf8");
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const categories = ["agents", "rag"].map((id) => ({ id, title: id.toUpperCase(), short: id, blurb: `${id} projects`, count: 2 }));
const repos = [
  { name: "alpha", category: "agents", stars: 50, stars_delta: 1, starred_at: "2026-01-01", pushed_at: "2026-04-01" },
  { name: "bravo", category: "rag", stars: 200, stars_delta: 4, starred_at: "2026-03-01", pushed_at: "2026-02-01", tags: ["agents"], mine: true, health: "dormant" },
  { name: "charlie", category: "agents", stars: 100, stars_delta: 8, starred_at: "2026-02-01", pushed_at: "2026-03-01", mine: true },
  { name: "delta", category: "rag", stars: 10, stars_delta: null, starred_at: "2026-04-01", pushed_at: "2026-01-01", health: "archived" },
].map((r) => ({ owner: "example", full_name: `example/${r.name}`, url: `https://github.com/example/${r.name}`, description: `${r.name} toolkit`, topics: ["shared"], tags: [], health: "active", ...r }));

function element(id, attributes = {}) {
  let markup = "";
  return {
    attributes, dataset: {}, children: [], value: "", checked: false, events: {},
    clientWidth: 600, clientHeight: 380,
    classList: { remove() {} },
    addEventListener(event, handler) { this.events[event] = handler; },
    setAttribute(name, value) { this.attributes[name] = String(value); },
    matches() { return id === "map" || id === "rail"; },
    get innerHTML() { return markup; },
    set innerHTML(value) {
      markup = value;
      this.children = [...value.matchAll(/<button\b([^>]*)>/g)].map((match) => {
        const attrs = Object.fromEntries([...match[1].matchAll(/([\w-]+)="([^"]*)"/g)].map((a) => [a[1], a[2]]));
        const button = element(id, attrs);
        button.dataset = { cat: attrs["data-cat"], sort: attrs["data-sort"] };
        return button;
      });
    },
  };
}

async function openPage(hash = "", data = {}) {
  const nodes = Object.fromEntries([...html.matchAll(/id="([^"]+)"/g)].map((match) => [match[1], element(match[1])]));
  nodes.sort.innerHTML = html.match(/id="sort">([\s\S]*?)<\/div>/)[1];
  const events = {};
  const documentEvents = {};
  const location = { hash, pathname: "/site/index.html", search: "" };
  const document = {
    documentElement: { dataset: {} },
    querySelector: (selector) => nodes[selector.slice(1)],
    querySelectorAll: (selector) => selector === "#sort button" ? nodes.sort.children : [nodes.map, nodes.rail, nodes.list].flatMap((node) => node.children),
    addEventListener: (event, handler) => { documentEvents[event] = handler; },
  };
  runInNewContext(script, {
    URL, URLSearchParams, location, document,
    addEventListener: (event, handler) => { events[event] = handler; },
    localStorage: { getItem() { return null; } },
    matchMedia: () => ({ matches: false, addEventListener() {} }),
    ResizeObserver: class { observe() {} },
    fetch: async () => ({ ok: true, json: async () => structuredClone({ categories, repos, user: "example", generated_at: "2026-10-08", tagline: "Test projects", ...data }) }),
    history: { replaceState(_state, _unused, url) { location.hash = url.startsWith("#") ? url : ""; } },
  });
  await new Promise(setImmediate);
  return {
    nodes, location, document, documentEvents,
    names: () => [...nodes.list.innerHTML.matchAll(/href="https:\/\/github\.com\/example\/([^"]+)"/g)].map((match) => match[1]),
    selectedSort: () => nodes.sort.children.filter((button) => button.attributes["aria-pressed"] === "true").map((button) => button.dataset.sort),
    selectedCategories: (id) => nodes[id].children.filter((button) => button.attributes["aria-pressed"] === "true").map((button) => button.dataset.cat),
    navigate(nextHash) { location.hash = nextHash; events.hashchange(); },
    change(id, value) { nodes[id].value = value; nodes[id].events.change({ target: nodes[id] }); },
    click(id) { documentEvents.click({ target: { closest: (selector) => selector === `#${id}` ? nodes[id] : null } }); },
  };
}

const byStars = ["bravo", "charlie", "alpha", "delta"];

for (const sort of ["garbage", "__proto__", "toString", "constructor", "hasOwnProperty"]) {
  test(`invalid sort ${sort} uses stars on load and hash change`, async () => {
    const page = await openPage(`#sort=${sort}`);
    assert.deepEqual(page.names(), byStars);
    assert.deepEqual(page.selectedSort(), ["stars"]);
    page.navigate("#sort=pushed");
    assert.deepEqual(page.names(), ["alpha", "charlie", "bravo", "delta"]);
    page.navigate(`#sort=${sort}`);
    assert.deepEqual(page.names(), byStars);
    assert.deepEqual(page.selectedSort(), ["stars"]);
  });
}

test("valid sort links retain their order and selected controls", async () => {
  for (const [sort, names] of Object.entries({ stars: byStars, momentum: ["charlie", "bravo", "alpha", "delta"], starred: ["delta", "bravo", "charlie", "alpha"], pushed: ["alpha", "charlie", "bravo", "delta"] })) {
    const page = await openPage(`#sort=${sort}`);
    assert.deepEqual(page.names(), names);
    assert.deepEqual(page.selectedSort(), [sort]);
  }
});

test("valid category links include related projects after primary matches", async () => {
  const page = await openPage("#cat=agents");
  assert.deepEqual(page.names(), ["charlie", "alpha", "bravo"]);
  assert.equal(page.nodes["h-title"].textContent, "AGENTS");
  assert.equal(page.nodes["h-count"].textContent, "2 projects, 1 related");
  assert.deepEqual(page.selectedCategories("rail"), ["agents"]);
  assert.deepEqual(page.selectedCategories("map"), ["agents"]);
});

for (const cat of ["unknown", "__proto__", "toString", "constructor"]) {
  test(`invalid category ${cat} uses all projects and preserves other filters`, async () => {
    const page = await openPage(`#cat=${cat}`);
    assert.deepEqual(page.names(), byStars);
    assert.equal(page.nodes["h-title"].textContent, "All projects");
    assert.deepEqual(page.selectedCategories("rail"), ["all"]);
    assert.deepEqual(page.selectedCategories("map"), []);
    page.navigate("#cat=agents");
    page.navigate(`#cat=${cat}&q=SHARED&sort=pushed&mine=1&active=1`);
    assert.deepEqual(page.names(), ["charlie"]);
    assert.equal(page.nodes.q.value, "SHARED");
    assert.equal(page.nodes.mine.checked, true);
    assert.equal(page.nodes.active.checked, true);
    assert.deepEqual(page.selectedSort(), ["pushed"]);
    assert.deepEqual(page.selectedCategories("rail"), ["all"]);
    assert.deepEqual(page.selectedCategories("map"), []);
  });
}

test("search links preserve all-term matching and checkbox URL semantics", async () => {
  const page = await openPage("#q=ALPHA+shared&mine=true&active=true");
  assert.deepEqual(page.names(), ["alpha"]);
  assert.equal(page.nodes.q.value, "ALPHA shared");
  assert.equal(page.nodes.mine.checked, false);
  assert.equal(page.nodes.active.checked, false);
  page.navigate("#cat=rag&q=shared&mine=1");
  assert.deepEqual(page.names(), ["bravo"]);
  page.navigate("#cat=rag&q=shared&mine=1&active=1");
  assert.deepEqual(page.names(), []);
  assert.match(page.nodes.list.innerHTML, /Nothing matches these filters/);
});

const comparisonRepos = [
  { ...repos[0], language: "Python", license: "MIT", maturity: { stage: "experimental", source: null, note: "Early development" } },
  { ...repos[1], language: "Python", license: "GPL-3.0", maturity: { stage: "beta", source: null, note: "" } },
  { ...repos[2], language: "JavaScript", license: "MIT", health: "maintained", maturity: { stage: "stable", source: "https://example.org/releases?channel=stable&view=all", note: "Declared stable channel" } },
  { ...repos[3], language: "", license: "", maturity: { stage: "unknown", source: null, note: "" } },
  { ...repos[0], name: "echo", full_name: "example/echo", url: "https://github.com/example/echo", stars: 5, health: null, language: null },
];

for (const [key, cases] of Object.entries({
  lang: { Python: ["bravo", "alpha"], JavaScript: ["charlie"], "~missing": ["delta", "echo"] },
  license: { MIT: ["charlie", "alpha"], "GPL-3.0": ["bravo"], "~missing": ["delta", "echo"] },
  stage: { experimental: ["alpha"], alpha: [], beta: ["bravo"], stable: ["charlie"], unknown: ["delta", "echo"] },
  health: { active: ["alpha"], maintained: ["charlie"], dormant: ["bravo"], archived: ["delta"], unknown: ["echo"] },
})) {
  test(`${key} filters from shared links and select changes`, async () => {
    for (const [value, names] of Object.entries(cases)) {
      const page = await openPage(`#${new URLSearchParams({ [key]: value })}`, { repos: comparisonRepos });
      assert.deepEqual(page.names(), names);
      assert.equal(page.nodes[key].value, value);
      assert.equal(page.nodes["clear-comparison"].disabled, false);
      page.change(key, "");
      assert.equal(new URLSearchParams(page.location.hash.slice(1)).has(key), false);
      assert.deepEqual(page.names(), ["bravo", "charlie", "alpha", "delta", "echo"]);
      page.change(key, value);
      assert.deepEqual(page.names(), names);
      assert.equal(new URLSearchParams(page.location.hash.slice(1)).get(key), value);
    }
  });
}

test("comparison options use the complete dataset and retain exact language/license values", async () => {
  const special = { ...comparisonRepos[0], language: "C++", license: "Apache-2.0" };
  const page = await openPage("#q=charlie&lang=JavaScript", { repos: [...comparisonRepos, special] });
  assert.match(page.nodes.lang.innerHTML, /value="C\+\+">C\+\+</);
  assert.match(page.nodes.lang.innerHTML, /value="Python">Python</);
  assert.match(page.nodes.lang.innerHTML, /value="~missing">Not specified</);
  assert.match(page.nodes.license.innerHTML, /value="Apache-2.0">Apache-2.0</);
  assert.match(page.nodes.stage.innerHTML, /value="alpha">Alpha</);
  page.navigate("#lang=C%2B%2B&license=Apache-2.0");
  assert.deepEqual(page.names(), ["alpha"]);
  assert.equal(page.nodes.lang.value, "C++");
});

test("all four comparisons combine with search, category, original work, and activity", async () => {
  const page = await openPage("#cat=agents&q=shared&mine=1&lang=Python&license=GPL-3.0&stage=beta&health=dormant", { repos: comparisonRepos });
  assert.deepEqual(page.names(), ["bravo"]);
  assert.equal(page.nodes["h-count"].textContent, '0 projects, 1 related matching "shared"');
  page.navigate(page.location.hash + "&active=1");
  assert.deepEqual(page.names(), []);
  assert.match(page.nodes.list.innerHTML, /Nothing matches these filters/);
  page.click("clear-comparison");
  assert.deepEqual(page.names(), ["charlie"]);
  const params = new URLSearchParams(page.location.hash.slice(1));
  assert.deepEqual(Object.fromEntries(params), { cat: "agents", q: "shared", mine: "1", active: "1" });
  assert.equal(page.nodes["clear-comparison"].disabled, true);
});

test("missing comparisons combine with AND and unknown maintenance", async () => {
  const page = await openPage("#lang=%7Emissing&license=%7Emissing&stage=unknown&health=archived", { repos: comparisonRepos });
  assert.deepEqual(page.names(), ["delta"]);
  page.change("health", "unknown");
  assert.deepEqual(page.names(), ["echo"]);
  page.change("license", "MIT");
  assert.deepEqual(page.names(), []);
  page.click("reset");
  assert.deepEqual(page.names(), ["bravo", "charlie", "alpha", "delta", "echo"]);
  assert.equal(page.location.hash, "");
});

test("comparison clear preserves search, category, sort, and checkbox controls", async () => {
  const page = await openPage("#cat=agents&q=shared&sort=pushed&mine=1&active=1&lang=JavaScript&license=MIT&stage=stable&health=maintained", { repos: comparisonRepos });
  page.click("clear-comparison");
  assert.deepEqual(Object.fromEntries(new URLSearchParams(page.location.hash.slice(1))), { cat: "agents", q: "shared", sort: "pushed", mine: "1", active: "1" });
  assert.deepEqual(page.selectedSort(), ["pushed"]);
  for (const key of ["lang", "license", "stage", "health"]) assert.equal(page.nodes[key].value, "");
});

test("hash navigation restores and clears all comparison controls", async () => {
  const page = await openPage("#lang=Python&license=MIT&stage=experimental&health=active", { repos: comparisonRepos });
  const previous = page.location.hash;
  page.navigate("#lang=JavaScript&license=MIT&stage=stable&health=maintained");
  assert.deepEqual(page.names(), ["charlie"]);
  page.navigate(previous);
  assert.deepEqual(page.names(), ["alpha"]);
  assert.equal(page.nodes.lang.value, "Python");
  assert.equal(page.nodes.license.value, "MIT");
  assert.equal(page.nodes.stage.value, "experimental");
  assert.equal(page.nodes.health.value, "active");
  page.navigate("#q=charlie");
  assert.deepEqual(page.names(), ["charlie"]);
  for (const key of ["lang", "license", "stage", "health"]) assert.equal(page.nodes[key].value, "");
});

test("invalid and prototype comparison values are ignored on load and navigation", async () => {
  for (const value of ["garbage", "__proto__", "constructor", "toString", "hasOwnProperty"]) {
    const hash = `#q=shared&cat=agents&sort=pushed&lang=${value}&license=${value}&stage=${value}&health=${value}`;
    const page = await openPage(hash, { repos: comparisonRepos });
    assert.deepEqual(page.names(), ["alpha", "echo", "charlie", "bravo"]);
    for (const key of ["lang", "license", "stage", "health"]) assert.equal(page.nodes[key].value, "");
    page.navigate("#stage=beta&health=dormant");
    assert.deepEqual(page.names(), ["bravo"]);
    page.navigate(hash);
    assert.deepEqual(page.names(), ["alpha", "echo", "charlie", "bravo"]);
    page.change("lang", "Python");
    assert.deepEqual(Object.fromEntries(new URLSearchParams(page.location.hash.slice(1))), { cat: "agents", q: "shared", sort: "pushed", lang: "Python" });
  }
});

test("stage is independent from health, popularity, and invalid maturity", async () => {
  const data = { repos: [
    { ...comparisonRepos[0], health: "dormant", maturity: { stage: "stable" } },
    { ...comparisonRepos[1], health: "active", maturity: { stage: "experimental" } },
    { ...comparisonRepos[2], health: "active", maturity: { stage: "constructor" } },
    { ...comparisonRepos[3], health: "active", maturity: "stable" },
    { ...comparisonRepos[4], health: "toString", maturity: ["stable"] },
  ] };
  const page = await openPage("#stage=stable&health=dormant", data);
  assert.deepEqual(page.names(), ["alpha"]);
  assert.match(page.nodes.list.innerHTML, /Development stage: Stable/);
  page.navigate("#stage=experimental&health=active");
  assert.deepEqual(page.names(), ["bravo"]);
  page.navigate("#stage=unknown&health=active");
  assert.deepEqual(page.names(), ["charlie", "delta"]);
  assert.match(page.nodes.list.innerHTML, /Development stage: Not assessed/);
  page.navigate("#health=unknown");
  assert.deepEqual(page.names(), ["echo"]);
});

test("legacy datasets show unassessed stages without classification badges", async () => {
  const page = await openPage("#stage=unknown");
  assert.deepEqual(page.names(), byStars);
  assert.equal([...page.nodes.list.innerHTML.matchAll(/Development stage: Not assessed/g)].length, 4);
  assert.doesNotMatch(page.nodes.list.innerHTML, /Review classification|Stage source/);
});

test("non-string stage and health values cannot be coerced into supported labels", async () => {
  for (const maturity of [null, {}, "stable", ["stable"], { stage: ["stable"] }, { stage: { toString: "stable" } }, { stage: false }]) {
    const page = await openPage("#stage=unknown&health=unknown", { repos: [{ ...comparisonRepos[0], maturity, health: ["active"] }] });
    assert.deepEqual(page.names(), ["alpha"]);
    assert.match(page.nodes.list.innerHTML, /Development stage: Not assessed/);
    assert.doesNotMatch(page.nodes.list.innerHTML, /Stage source/);
  }
});

test("stage source is independently validated as an HTTPS URL", async () => {
  for (const source of ["javascript:alert(1)", "data:text/html,unsafe", "http://example.org", "//example.org", "/releases", "https://", "https://user:secret@example.org", null, { href: "https://example.org" }]) {
    const page = await openPage("", { repos: [{ ...comparisonRepos[0], maturity: { stage: "stable", source } }] });
    assert.deepEqual(page.names(), ["alpha"]);
    assert.doesNotMatch(page.nodes.list.innerHTML, /Stage source/);
    assert.match(page.nodes.list.innerHTML, /Development stage: Stable/);
  }
  const page = await openPage("#stage=stable", { repos: comparisonRepos });
  assert.match(page.nodes.list.innerHTML, /href="https:\/\/example.org\/releases\?channel=stable&amp;view=all" target="_blank" rel="noopener noreferrer"/);
  assert.match(page.nodes.list.innerHTML, /title="Declared stable channel"/);
});

test("new option labels, stage notes, and classification details escape external text", async () => {
  const hostile = '"><img src=x onerror=alert(1)>';
  const page = await openPage("", { repos: [{ ...comparisonRepos[0], language: hostile, license: hostile, maturity: { stage: "stable", source: "https://example.org/", note: hostile }, classification: { review_needed: true, reasons: ["low_score", "close_scores", hostile], score: 3, margin: 0, runner_up: hostile, runner_up_score: 3 } }] });
  for (const markup of [page.nodes.lang.innerHTML, page.nodes.license.innerHTML, page.nodes.list.innerHTML]) {
    assert.doesNotMatch(markup, /<img src=x|title=""><img|value=""><img/);
    assert.match(markup, /&quot;&gt;&lt;img src=x onerror=alert\(1\)&gt;/);
  }
  assert.match(page.nodes.list.innerHTML, /Review classification/);
  assert.match(page.nodes.list.innerHTML, /Low rule score\. Close category scores/);
  assert.match(page.nodes.list.innerHTML, /Rule score: 3\. Score margin: 0\. Alternative: &quot;/);
  assert.doesNotMatch(page.nodes.list.innerHTML, /confidence|[0-9]+%/i);
});

test("classification badge uses known candidate labels and strictly requires review_needed true", async () => {
  const page = await openPage("", { repos: [{ ...comparisonRepos[0], classification: { review_needed: true, reasons: ["unmatched", "manual_triage"], score: 0, margin: 1, runner_up: "rag", runner_up_score: 2 } }] });
  assert.match(page.nodes.list.innerHTML, /No matching rule\. Manual triage requested\. Rule score: 0\. Score margin: 1\. Alternative: RAG \(score 2\)/);
  assert.match(page.nodes.list.innerHTML, /class="badge review" tabindex="0"/);
  assert.match(page.nodes.list.innerHTML, /aria-label="Review classification: No matching rule/);
  for (const classification of [null, {}, { review_needed: false }, { review_needed: "true" }]) {
    const legacy = await openPage("", { repos: [{ ...comparisonRepos[0], classification }] });
    assert.doesNotMatch(legacy.nodes.list.innerHTML, /Review classification/);
  }
});

test("comparison changes, clear, and hash navigation reset pagination", async () => {
  const data = { repos: Array.from({ length: 45 }, (_, i) => ({ ...comparisonRepos[0], name: `project${i}`, url: `https://github.com/example/project${i}` })) };
  const page = await openPage("", data);
  assert.equal(page.names().length, 40);
  page.click("more-btn");
  assert.equal(page.names().length, 45);
  page.change("lang", "Python");
  assert.equal(page.names().length, 40);
  page.click("more-btn");
  page.click("clear-comparison");
  assert.equal(page.names().length, 40);
  page.click("more-btn");
  page.navigate("#license=MIT");
  assert.equal(page.names().length, 40);
  assert.equal(page.nodes.more.hidden, false);
});

test("search shortcut respects focused comparison selects", async () => {
  const page = await openPage();
  page.document.activeElement = { tagName: "SELECT" };
  let prevented = false;
  page.documentEvents.keydown({ key: "/", preventDefault() { prevented = true; } });
  assert.equal(prevented, false);
});
