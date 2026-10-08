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
    attributes, dataset: {}, children: [], value: "", checked: false,
    clientWidth: 600, clientHeight: 380,
    classList: { remove() {} },
    addEventListener() {},
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

async function openPage(hash) {
  const nodes = Object.fromEntries([...html.matchAll(/id="([^"]+)"/g)].map((match) => [match[1], element(match[1])]));
  nodes.sort.innerHTML = html.match(/id="sort">([\s\S]*?)<\/div>/)[1];
  const events = {};
  const location = { hash, pathname: "/site/index.html", search: "" };
  runInNewContext(script, {
    URLSearchParams, location,
    document: {
      documentElement: { dataset: {} },
      querySelector: (selector) => nodes[selector.slice(1)],
      querySelectorAll: (selector) => selector === "#sort button" ? nodes.sort.children : [nodes.map, nodes.rail, nodes.list].flatMap((node) => node.children),
      addEventListener() {},
    },
    addEventListener: (event, handler) => { events[event] = handler; },
    localStorage: { getItem() { return null; } },
    matchMedia: () => ({ matches: false, addEventListener() {} }),
    ResizeObserver: class { observe() {} },
    fetch: async () => ({ ok: true, json: async () => structuredClone({ categories, repos, user: "example", generated_at: "2026-10-08", tagline: "Test projects" }) }),
    history: { replaceState() {} },
  });
  await new Promise(setImmediate);
  return {
    nodes,
    names: () => [...nodes.list.innerHTML.matchAll(/href="https:\/\/github\.com\/example\/([^"]+)"/g)].map((match) => match[1]),
    selectedSort: () => nodes.sort.children.filter((button) => button.attributes["aria-pressed"] === "true").map((button) => button.dataset.sort),
    selectedCategories: (id) => nodes[id].children.filter((button) => button.attributes["aria-pressed"] === "true").map((button) => button.dataset.cat),
    navigate(nextHash) { location.hash = nextHash; events.hashchange(); },
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
