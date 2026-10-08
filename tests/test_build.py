import copy
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import build  # noqa: E402

CFG = build.load_config()
FIXTURE = json.loads((HERE / "fixture.json").read_text(encoding="utf-8"))
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


class ForkTest(unittest.TestCase):
    def fresh(self):
        return build.load_config()

    def test_original_repo_is_untouched(self):
        for repo in ("alebgl77/awesome-ai-architect", "AleBgl77/Awesome-AI-Architect"):
            with self.subTest(repo=repo):
                cfg = self.fresh()
                original = copy.deepcopy(cfg)
                self.assertIs(build.adapt_for_fork(cfg, {"GITHUB_REPOSITORY": repo}), cfg)
                self.assertEqual(cfg, original)

    def test_same_owner_copy_takes_repository_identity(self):
        cfg = build.adapt_for_fork(self.fresh(), {"GITHUB_REPOSITORY": "alebgl77/my-copy"})
        lst = cfg["list"]
        self.assertEqual((lst["user"], lst["repo"]), ("alebgl77", "alebgl77/my-copy"))
        self.assertEqual(lst["site_url"], "https://alebgl77.github.io/awesome-ai-architect/?repo=alebgl77/my-copy")
        self.assertEqual(lst["exclude_own"], ["alebgl77", "my-copy"])
        self.assertEqual(cfg["overrides"], {})

    def test_configured_repository_preserves_custom_user(self):
        cfg = self.fresh()
        cfg["list"].update(repo="JaneDev/my-ai-map", user="CuratedAccount", author="Custom Author")
        original = copy.deepcopy(cfg)
        env = {"GITHUB_REPOSITORY": "JaneDev/my-ai-map", "GITHUB_REPOSITORY_OWNER": "JaneDev"}
        self.assertEqual(build.adapt_for_fork(cfg, env), original)

    def test_fork_takes_owner_identity(self):
        env = {"GITHUB_REPOSITORY": "JaneDev/my-ai-map", "GITHUB_REPOSITORY_OWNER": "JaneDev"}
        lst = build.adapt_for_fork(self.fresh(), env)["list"]
        self.assertEqual((lst["user"], lst["repo"]), ("JaneDev", "JaneDev/my-ai-map"))
        self.assertEqual(lst["site_url"], "https://alebgl77.github.io/awesome-ai-architect/?repo=JaneDev/my-ai-map")
        self.assertEqual(lst["exclude_own"], ["JaneDev", "my-ai-map"])

    def test_fork_drops_owner_overrides(self):
        cfg = build.adapt_for_fork(self.fresh(), {"GITHUB_REPOSITORY": "x/y"})
        self.assertEqual(cfg["overrides"], {})

    def test_local_run_is_untouched(self):
        self.assertEqual(build.adapt_for_fork(self.fresh(), {})["list"]["user"], "alebgl77")


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
            hist = json.loads(hist_path.read_text(encoding="utf-8"))
            hist["2026-09-26"]["vllm-project/vllm"] -= 500
            hist_path.write_text(json.dumps(hist), encoding="utf-8")
            data = run_fixture(Path(tmp))
            vllm = next(r for r in data["repos"] if r["full_name"] == "vllm-project/vllm")
            self.assertEqual((vllm["stars_delta"], vllm["delta_days"]), (500, 7))
            self.assertIn("## Rising", (Path(tmp) / "README.md").read_text(encoding="utf-8"))


class RenderTest(unittest.TestCase):
    def test_readme_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_fixture(Path(tmp))
            md = (Path(tmp) / "README.md").read_text(encoding="utf-8")
        self.assertTrue(md.startswith("# Awesome AI Architect"))
        for heading in ("## Built by Alexandre", "## Recently starred", "## MCP & Tool Use", "## How it works"):
            self.assertIn(heading, md)
        self.assertNotIn("## To Triage", md)
        self.assertIn("/generate)", md)
        self.assertNotIn("/fork)", md)
        self.assertIn("placed by the rules alone", md)
        self.assertIn("(#rag-retrieval--knowledge)", md)

    def test_pipes_in_descriptions_are_escaped(self):
        repo = build.normalize({"full_name": "a/b", "description": "x | y"}, None, False)
        build.classify([repo], CFG)
        repo.update(health="active", stars_delta=None)
        self.assertIn("x \\| y", build._row(repo, {c["id"]: c["title"] for c in CFG["category"]}))

    def test_number_format(self):
        self.assertEqual([build.fmt_num(n) for n in (999, 1000, 93128, 2_000_000)], ["999", "1k", "93.1k", "2M"])

    def test_momentum_has_one_sign_and_omits_zero(self):
        repo = build.normalize({"full_name": "a/b"}, None, False)
        titles = {c["id"]: c["title"] for c in CFG["category"]}
        for delta, expected in ((2, " <sub>+2</sub>"), (-2, " <sub>-2</sub>"),
                                (1000, " <sub>+1k</sub>"), (-1000, " <sub>-1k</sub>"),
                                (0, ""), (None, "")):
            with self.subTest(delta=delta):
                repo["stars_delta"] = delta
                row = build._row(repo, titles)
                self.assertIn(f" | 0{expected} | ", row)
                self.assertNotIn("+-", row)

    def test_rising_only_contains_positive_momentum(self):
        repos = []
        for name, delta in (("falling", -2), ("steady", 0), ("unknown", None),
                            ("rising", 2), ("fastest", 10), ("own", 20)):
            repo = build.normalize({"full_name": f"sample/{name}"}, None, name == "own")
            build.classify([repo], CFG)
            repo.update(stars_delta=delta, delta_days=7 if delta is not None else None)
            repos.append(repo)
        md = build.render_readme(repos, CFG, TODAY)
        rising = md.split("## Rising\n", 1)[1].split("\n## ", 1)[0]
        self.assertLess(rising.index("[**fastest**]"), rising.index("[**rising**]"))
        for name in ("falling", "steady", "unknown", "own"):
            self.assertNotIn(f"[**{name}**]", rising)
        md = build.render_readme(repos[:3], CFG, TODAY)
        self.assertNotIn("## Rising", md)
        self.assertNotIn("[Rising](#rising)", md)


class EncodingTest(unittest.TestCase):
    def test_cli_preserves_unicode_without_utf8_mode(self):
        description = "Café — 東京 🚀"
        payload = {"starred": [{"full_name": "sample/unicode", "description": description,
                                "stargazers_count": 12, "topics": ["inference"]}], "own": []}
        env = {k: v for k, v in os.environ.items()
               if k not in ("GITHUB_REPOSITORY", "GITHUB_REPOSITORY_OWNER")}
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            fixture = out / "fixture.json"
            fixture.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            data_dir = out / "data"
            data_dir.mkdir()
            history_path = data_dir / "history.json"
            history = {"2026-09-26": {"sample/unicode": 10, "sample/東京": 1}}
            history_path.write_text(json.dumps(history, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-X", "utf8=0", "-X", "warn_default_encoding", "-W", "error::EncodingWarning",
                 str(HERE.parent / "scripts" / "build.py"), "--fixture", str(fixture),
                 "--today", TODAY.isoformat(), "--out", str(out)],
                env=env, capture_output=True, text=True, encoding="utf-8", timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            dataset = json.loads((data_dir / "repos.json").read_text(encoding="utf-8"))
            self.assertEqual(dataset["repos"][0]["description"], description)
            self.assertEqual(dataset["repos"][0]["stars_delta"], 2)
            self.assertIn(description, (out / "README.md").read_text(encoding="utf-8"))
            self.assertEqual(json.loads(history_path.read_text(encoding="utf-8"))["2026-09-26"],
                             history["2026-09-26"])


if __name__ == "__main__":
    unittest.main()
