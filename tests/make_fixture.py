"""Builds tests/fixture.json from real GitHub metadata snapshots (October 2026)."""
import json
from pathlib import Path

OWN = [
 ("claude-inc","Your project, an entire virtual company. CEO and CTO, 8 business departments and 54 skill manuals in Claude Code.","Python",16,"agentic-ai ai-agents automation claude claude-code claude-code-plugin claude-skills developer-tools llm multi-agent productivity","2026-07-11","2026-09-27"),
 ("tierdecay","Per-repo learning layer for AI coding model routers: learns which task classes can safely run on a cheaper tier. Native for Claude Code, Codex, Antigravity · MCP server · zero deps.","JavaScript",1,"agent-skills agents-md ai-agents ai-coding claude-code cost-optimization developer-tools finops google-antigravity llm llmops mcp model-context-protocol model-routing openai-codex","2026-07-12","2026-10-02"),
 ("grafana-llmops-forge","Grafana-native LLMOps dashboards for FinOps, agents, quality and AI governance, generated and visually verified.","Python",1,"agent-skills ai-governance ai-observability claude-code claude-skills eu-ai-act finops grafana grafana-dashboards litellm llm-observability llmops opentelemetry prometheus sre vllm","2026-07-12","2026-09-14"),
 ("open-fullscreenshot","Full-page screen capture extension for Chrome (Manifest V3) — scroll-and-stitch full page, visible area, element or region. activeTab only, no host permissions, no network, no telemetry.","JavaScript",0,"","2026-08-12","2026-09-14"),
 ("promptor","Architecte de prompts sur mesure — protocole itératif human-in-the-loop avec mémoire apprenante, pour ChatGPT, Claude, Gemini, Midjourney, Cursor et agents","",0,"ai chatgpt claude francais gemini llm meta-prompt midjourney prompt-engineering","2026-07-19","2026-07-20"),
 ("generative-engine-monitor","Measure brand visibility in AI answers with explainable scoring, confidence intervals and zero-cost replay.","TypeScript",0,"aeo ai-search anthropic brand-monitoring geo llm nextjs openai perplexity postgresql prisma typescript","2026-08-03","2026-09-14"),
 ("dsh-plugin-otel-genai","OpenTelemetry GenAI metrics for DeepSeek Harness: token usage and step latency per provider and model, exported over OTLP for Grafana and Prometheus","TypeScript",0,"deepseek-harness dsh-plugin grafana llmops opentelemetry","2026-09-06","2026-09-14"),
 ("harnessmeter","Offline profiler for AI agent instructions, skills, subagents and MCP schemas. No API keys or network.","TypeScript",0,"agent-harness ai-agents claude-code claude-md context-engineering developer-tools harness-engineering llm mcp observability profiler prompt-engineering","2026-07-27","2026-09-26"),
 ("design-md-viewer","Client-side explorer that parses a design-system markdown file into browsable tokens, a health audit and code exports.","TypeScript",0,"accessibility design-md design-system design-tokens markdown react tailwindcss typescript vite wcag","2026-08-20","2026-09-14"),
 ("alebgl77","Profile and open-source work of Alexandre Beguel.","",0,"","2026-06-18","2026-09-14"),
 ("ftp-deploy-mcp","MCP server to deploy, inspect and transfer files over FTP/FTPS/SFTP from AI coding agents. Local confinement, SFTP host-key pinning, verified staged promotion, read-only mode and dry runs. Bilingual EN/FR.","HTML",0,"ai-agents ai-coding claude claude-code cursor deployment deployment-automation devops filezilla ftp ftps mcp mcp-server mcp-tools model-context-protocol nodejs secure-deployment sftp shared-hosting windsurf","2026-07-20","2026-09-26"),
 ("openspanguard","Make AI quality observable. OpenTelemetry trace enrichment, Jev evaluation, streaming deduplication, and cohort quality alerts.","TypeScript",0,"ai-agents ai-observability genai grafana jev llm-evaluation llm-monitoring llmops observability opentelemetry otlp prometheus quality-monitoring typescript","2026-09-26","2026-09-27"),
 ("open-shadow-ai","Self-hosted Shadow AI discovery and governance. Evidence-first visibility across network, endpoints, Active Directory and Entra ID.","Python",0,"active-directory ai-governance cybersecurity docker entra-id fastapi kubernetes react self-hosted shadow-ai","2026-09-26","2026-09-27"),
]
STARS = [
 ("n8n-io/n8n","Fair-code workflow automation platform with native AI capabilities. Combine visual building with custom code, self-host or cloud, 400+ integrations.","TypeScript",206587,"ai apis automation cli data-flow development integration-framework integrations ipaas low-code low-code-platform mcp mcp-client mcp-server n8n no-code self-hosted typescript workflow workflow-automation"),
 ("ollama/ollama","Get up and running with Kimi, GLM, MiniMax, DeepSeek, gpt-oss, Qwen, Gemma and other models.","Go",182113,"deepseek gemma gemma3 glm go golang gpt-oss llama llama3 llm llms minimax mistral ollama qwen"),
 ("huggingface/transformers","🤗 Transformers: the model-definition framework for state-of-the-art machine learning models in text, vision, audio, and multimodal models, for both inference and training.","Python",166926,"audio deep-learning deepseek gemma glm hacktoberfest llm machine-learning model-hub natural-language-processing nlp pretrained-models python pytorch pytorch-transformers qwen speech-recognition transformer vlm"),
 ("anthropics/claude-code","Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands.","TypeScript",149204,""),
 ("Shubhamsaboo/awesome-llm-apps","100+ AI Agents, Agent Skills and RAG Apps - Free and Open Source.","Python",140632,"agents llms python rag"),
 ("shadcn-ui/ui","Composable, accessible components with thoughtful defaults. Build your own component library with code you can customize, extend, and make your own.","TypeScript",125055,"base-ui components laravel nextjs radix-ui react react-aria react-aria-components shadcn tailwindcss tanstack ui vite"),
 ("browser-use/browser-use","Agents that use the browser.","Python",117069,"ai-agents ai-tools browser-automation browser-use llm playwright python"),
 ("openai/whisper","Robust Speech Recognition via Large-Scale Weak Supervision","Python",109919,""),
 ("punkpeye/awesome-mcp-servers","A collection of MCP servers.","",95791,"ai mcp"),
 ("vllm-project/vllm","A high-throughput and memory-efficient inference and serving engine for LLMs","Python",93128,"amd blackwell cuda deepseek deepseek-v3 gpt gpt-oss inference kimi llama llm llm-serving model-serving moe openai pytorch qwen qwen3 tpu transformer"),
 ("Leonxlnx/taste-skill","Taste-Skill - gives your AI good taste. stops the AI from generating boring, generic slop","JavaScript",92315,"agent ai claude claude-code codex coding design frontend lowcode nocode skill skills vibecoding"),
 ("modelcontextprotocol/servers","Model Context Protocol Servers","TypeScript",90985,""),
 ("unslothai/unsloth","Local UI to run and train LLMs and diffusion models. Supports GGUF, MLX, Qwen3.8, DeepSeek-V4, MiniMax-H3, Gemma 4, FLUX and more.","Python",77172,"agent ai chatgpt deepseek fine-tuning gemma image-generation llama llm llms openai python qwen reinforcement-learning self-hosted stable-diffusion text-to-speech tts ui unsloth"),
 ("docling-project/docling","Get your documents ready for gen AI","Python",68341,"ai convert document-parser document-parsing documents docx html markdown pdf pdf-converter pdf-to-json pdf-to-text pptx tables xlsx"),
 ("microsoft/autogen","A programming framework for agentic AI","Python",61250,"agentic agentic-agi agents ai autogen autogen-ecosystem chatgpt framework llm-agent llm-framework"),
 ("BerriAI/litellm","The fastest, litest AI Gateway. Rust core with Python SDK. Call 100+ LLM APIs in OpenAI (or native) format with cost tracking, guardrails, load balancing, and logging [Bedrock, Azure, OpenAI, Anthropic, OpenAI, VertexAI, vLLM, Nvidia NIM]","Python",60091,"ai-gateway anthropic azure-openai bedrock gateway langchain litellm llm llm-gateway llmops mcp-gateway openai openai-proxy rust rust-ai vertex-ai"),
 ("crewAIInc/crewAI","Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks.","Python",59324,"agents ai ai-agents aiagentframework llms"),
 ("run-llama/llama_index","LlamaIndex is the document processing platform for AI","Python",52397,"agents application data fine-tuning framework llamaindex llm multi-agents rag vector-database"),
 ("langchain-ai/langgraph","Build resilient agents.","Python",42676,"agents ai ai-agents chatgpt deepagents enterprise framework gemini generative-ai langchain langgraph llm multiagent open-source openai pydantic python rag"),
 ("stanfordnlp/dspy","DSPy: The framework for programming—not prompting—language models","Python",38488,""),
 ("microsoft/graphrag","A modular graph-based Retrieval-Augmented Generation (RAG) system","Python",36198,"gpt gpt-4 gpt4 graphrag llm llms rag"),
 ("langfuse/langfuse","🪢 Open source agent evals & observability: Trace, evaluate, and improve LLM applications with one open platform.","TypeScript",35347,"analytics autogen evaluation langchain large-language-models llama-index llm llm-evaluation llm-observability llmops monitoring observability open-source openai playground prompt-engineering prompt-management self-hosted ycombinator"),
 ("qdrant/qdrant","Qdrant - High-performance, massive-scale Vector Database and Vector Search Engine for the next generation of AI. Also available in the cloud https://cloud.qdrant.io/","Rust",34919,"ai-search ai-search-engine embeddings-similarity hnsw hybrid-search image-search knn-algorithm machine-learning mlops nearest-neighbor-search neural-network neural-search recommender-system search search-engine search-engines similarity-search vector-database vector-search vector-search-engine"),
 ("promptfoo/promptfoo","Test your prompts, agents, and RAGs. Red teaming/pentesting/vulnerability scanning for AI. Compare performance of GPT, Claude, Gemini, DeepSeek, and more. Simple declarative configs with command line and CI/CD integration.  Used by OpenAI and Anthropic.","TypeScript",25678,"ci ci-cd cicd evaluation evaluation-framework llm llm-eval llm-evaluation llm-evaluation-framework llmops pentesting prompt-engineering prompt-testing prompts rag red-teaming testing vulnerability-scanners"),
 ("protectai/llm-guard","The Security Toolkit for LLM Interactions","Python",3212,"adversarial-machine-learning chatgpt large-language-models llm llm-security llmops prompt-engineering prompt-injection security-tools transformers"),
 ("affaan-m/agentshield","AI agent security scanner. Detect vulnerabilities in agent configurations, MCP servers, and tool permissions. Available as CLI, GitHub Action, ECC plugin, and GitHub App integration. 🛡️","TypeScript",1248,"ai-agent anthropic claude-code hackathon mcp opus security"),
 ("grafana/plugin-tools","Create Grafana plugins with ease.","TypeScript",88,"grafana grafana-plugin group-datasources keep plugins-platform scaffolder team-grafana-catalog"),
]

def repo(full, desc, lang, stars, topics, created="2024-01-01", pushed="2026-10-01", private=False, archived=False):
    owner, name = full.split("/")
    return {"full_name": full, "name": name, "owner": {"login": owner}, "html_url": f"https://github.com/{full}",
            "description": desc, "language": lang or None, "stargazers_count": stars, "forks_count": stars // 8,
            "open_issues_count": 0, "topics": topics.split(), "created_at": created + "T00:00:00Z",
            "pushed_at": pushed + "T00:00:00Z", "license": {"spdx_id": "MIT"}, "private": private,
            "archived": archived, "fork": False, "homepage": ""}

own = [repo("alebgl77/" + n, d, l, s, t, c, p) for n, d, l, s, t, c, p in OWN]
own.append(repo("alebgl77/ai-quote-engine", "Private repo", "TypeScript", 0, "", private=True))
starred = []
for i, (full, d, l, s, t) in enumerate(STARS):
    starred.append({"starred_at": f"2026-09-{28 - i % 27:02d}T10:00:00Z",
                    "repo": repo(full, d, l, s, t, archived=full == "protectai/llm-guard")})
starred.append({"starred_at": "2026-09-01T10:00:00Z", "repo": repo("alebgl77/claude-inc", OWN[0][1], "Python", 16, OWN[0][4])})
Path(__file__).with_name("fixture.json").write_text(json.dumps({"own": own, "starred": starred}, ensure_ascii=False, indent=1))
