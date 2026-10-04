import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import build  # noqa: E402

CFG = build.load_config()
FIXTURE = json.loads((HERE / "fixture.json").read_text())
TODAY = dt.date(2026, 10, 3)


def run_fixture(out: Path, today: dt.date = TODAY) -> dict:
    return build.build(FIXTURE, CFG, today, out)


class ClassifyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.data = run_fixture(Path(cls.tmp.name))
        cls.by_name = {r["full_name"]: r for r in cls.data["repos"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def cat(self, name):
        return self.by_name[name]["category"]

    def test_reference_projects_land_in_expected_categories(self):
        expected = {
            "langchain-ai/langgraph": "agents",
            "crewAIInc/crewAI": "agents",
            "microsoft/graphrag": "rag",
            "qdrant/qdrant": "rag",
            "promptfoo/promptfoo": "evals",
            "langfuse/langfuse": "observability",
            "protectai/llm-guard": "security",
            "vllm-project/vllm": "inference",
            "BerriAI/litellm": "inference",
            "modelcontextprotocol/servers": "mcp",
            "anthropics/claude-code": "coding",
            "Leonxlnx/taste-skill": "coding",
            "stanfordnlp/dspy": "context",
            "openai/whisper": "multimodal",
            "n8n-io/n8n": "automation",
            "shadcn-ui/ui": "frontend",
            "alebgl77/ftp-deploy-mcp": "mcp",
            "alebgl77/generative-engine-monitor": "search",
            "alebgl77/openspanguard": "observability",
            "alebgl77/open-shadow-ai": "security",
        }
        wrong = {n: self.cat(n) for n, c in expected.items() if self.cat(n) != c}
        self.assertEqual(wrong, {})

    def test_secondary_tags_exclude_primary_and_are_capped(self):
        for r in self.data["repos"]:
            self.assertNotIn(r["category"], r["tags"])
            self.assertLessEqual(len(r["tags"]), CFG["scoring"]["max_secondary"])

    def test_unmatched_repo_goes_to_triage(self):
        repo = build.normalize({"full_name": "x/zzz", "description": "Lorem ipsum."}, None, False)
        build.classify([repo], CFG)
        self.assertEqual(repo["category"], "triage")
        self.assertEqual(repo["classified_by"], "none")

    def test_override_wins(self):
        cfg = {**CFG, "overrides": {"qdrant/qdrant": "learning"}}
        repo = dict(self.by_name["qdrant/qdrant"])
        build.classify([repo], cfg)
        self.assertEqual(repo["category"], "learning")
        self.assertEqual(repo["classified_by"], "override")

    def test_key_topics_explain_the_category(self):
        self.assertIn("inference", self.by_name["vllm-project/vllm"]["key_topics"])
        self.assertNotEqual(self.by_name["n8n-io/n8n"]["key_topics"][0], "ai")


class CollectTest(unittest.TestCase):
    def setUp(self):
        self.repos = {r["full_name"]: r for r in build.collect(FIXTURE, CFG)}

    def test_private_and_excluded_repos_are_dropped(self):
        self.assertNotIn("alebgl77/ai-quote-engine", self.repos)
        self.assertNotIn("alebgl77/alebgl77", self.repos)

    def test_starring_own_repo_keeps_it_mine_without_duplicate(self):
        repo = self.repos["alebgl77/claude-inc"]
        self.assertTrue(repo["mine"])
        self.assertEqual(repo["starred_at"], "2026-09-01T10:00:00Z")
        self.assertEqual(sum(1 for k in self.repos if k.endswith("/claude-inc")), 1)

    def test_starred_metadata(self):
        repo = self.repos["vllm-project/vllm"]
        self.assertFalse(repo["mine"])
        self.assertEqual(repo["license"], "MIT")
        self.assertTrue(repo["starred_at"].startswith("2026-09"))


class MomentumTest(unittest.TestCase):
    def test_delta_uses_oldest_snapshot_inside_30_days(self):
        repos = [{"full_name": "a/b", "stars": 150}, {"full_name": "c/d", "stars": 10}]
        history = {"2026-08-01": {"a/b": 1}, "2026-09-10": {"a/b": 100}, "2026-09-20": {"a/b": 120}}
        build.apply_momentum(repos, history, TODAY)
        self.assertEqual(repos[0]["stars_delta"], 50)
        self.assertEqual(repos[0]["delta_days"], 23)
        self.assertIsNone(repos[1]["stars_delta"])

    def test_history_is_pruned(self):
        hist = build.update_history([{"full_name": "a/b", "stars": 1}], {"2026-01-01": {}}, TODAY, 35)
        self.assertEqual(list(hist), ["2026-10-03"])

    def test_second_run_produces_momentum(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_fixture(Path(tmp), dt.date(2026, 9, 26))
            hist_path = Path(tmp) / "data" / "history.json"
            hist = json.loads(hist_path.read_text())
            hist["2026-09-26"]["vllm-project/vllm"] -= 500
            hist_path.write_text(json.dumps(hist))
            data = run_fixture(Path(tmp))
            vllm = next(r for r in data["repos"] if r["full_name"] == "vllm-project/vllm")
            self.assertEqual((vllm["stars_delta"], vllm["delta_days"]), (500, 7))
            self.assertIn("## Rising", (Path(tmp) / "README.md").read_text())


class RenderTest(unittest.TestCase):
    def test_readme_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_fixture(Path(tmp))
            md = (Path(tmp) / "README.md").read_text()
        self.assertTrue(md.startswith("# Awesome AI Architect"))
        for heading in ("## Built by Alexandre", "## Recently starred", "## MCP & Tool Use", "## How it works"):
            self.assertIn(heading, md)
        self.assertNotIn("## To Triage", md)
        self.assertIn("(#rag-retrieval--knowledge)", md)

    def test_pipes_in_descriptions_are_escaped(self):
        repo = build.normalize({"full_name": "a/b", "description": "x | y"}, None, False)
        build.classify([repo], CFG)
        repo.update(health="active", stars_delta=None)
        self.assertIn("x \\| y", build._row(repo, {c["id"]: c["title"] for c in CFG["category"]}))

    def test_number_format(self):
        self.assertEqual([build.fmt_num(n) for n in (999, 1000, 93128, 2_000_000)], ["999", "1k", "93.1k", "2M"])


if __name__ == "__main__":
    unittest.main()
