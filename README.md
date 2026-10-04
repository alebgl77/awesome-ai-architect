# Awesome AI Architect

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![GitHub stars](https://img.shields.io/github/stars/alebgl77/awesome-ai-architect?style=social)](https://github.com/alebgl77/awesome-ai-architect/stargazers) ![Projects](https://img.shields.io/badge/projects-94-0f766e) ![Updated](https://img.shields.io/badge/updated-2026--10--04-0f766e) ![Auto-classified](https://img.shields.io/badge/classified-automatically-0f766e) ![No API keys](https://img.shields.io/badge/API%20keys-none-0f766e)

> A self-updating map of the GenAI engineering stack: agents, RAG, MCP, evals, LLMOps and AI security. Classified automatically from the GitHub stars and open-source work of an AI architect.

**[Open the interactive explorer](https://alebgl77.github.io/awesome-ai-architect/)**: search, filter by category, sort by stars, momentum or recency.

82 starred projects and 12 original projects across 17 categories. Regenerated every day by GitHub Actions from [@alebgl77](https://github.com/alebgl77)'s stars: star a repository and it shows up here, classified, the next morning.

**Want this for your own stars?** [Fork it](https://github.com/alebgl77/awesome-ai-architect/fork), change one line, done. See [Use it for your own stars](#use-it-for-your-own-stars). If the map helps you, a star keeps it visible.

## Contents

- [Built by Alexandre](#built-by-alexandre) (12)
- [Recently starred](#recently-starred)
- [MCP & Tool Use](#mcp--tool-use) (3)
- [Agent Memory & Persistent Context](#agent-memory--persistent-context) (6)
- [Observability, LLMOps & FinOps](#observability-llmops--finops) (3)
- [AI Security, Safety & Governance](#ai-security-safety--governance) (5)
- [Generative Search, GEO & LLMO](#generative-search-geo--llmo) (2)
- [Prompt & Context Engineering](#prompt--context-engineering) (2)
- [AI Coding Agents & Skills](#ai-coding-agents--skills) (24)
- [Agent Frameworks & Orchestration](#agent-frameworks--orchestration) (11)
- [Inference, Serving & Model Routing](#inference-serving--model-routing) (2)
- [Models, Training & Fine-tuning](#models-training--fine-tuning) (1)
- [Vision, Voice & Generative Media](#vision-voice--generative-media) (3)
- [Data Engineering, Scraping & Analytics](#data-engineering-scraping--analytics) (2)
- [Automation, Browser Agents & Productivity](#automation-browser-agents--productivity) (6)
- [Frontend, Design & Generative UI](#frontend-design--generative-ui) (2)
- [Cloud, DevOps & Infrastructure](#cloud-devops--infrastructure) (3)
- [AI Apps & Chat Interfaces](#ai-apps--chat-interfaces) (4)
- [Learning, Papers & Awesome Lists](#learning-papers--awesome-lists) (3)
- [How it works](#how-it-works)
- [Use it for your own stars](#use-it-for-your-own-stars)
- [Suggest a project](#suggest-a-project)

## Built by Alexandre

Original open-source work, classified with the same taxonomy.

| Project | What it does | Stars | Category | Last push |
|:--|:--|--:|:--|:--|
| [**claude-inc**](https://github.com/alebgl77/claude-inc)<br><sub>alebgl77</sub> | Your project, an entire virtual company. CEO and CTO, 8 business departments and 54 skill manuals in Claude Code.<br><sub>`claude-code` `claude-skills` `claude-code-plugin` `agentic-ai`</sub> | 16 | AI Coding Agents & Skills | 2026-09 |
| [**grafana-llmops-forge**](https://github.com/alebgl77/grafana-llmops-forge)<br><sub>alebgl77</sub> | Grafana-native LLMOps dashboards for FinOps, agents, quality and AI governance, generated and visually verified.<br><sub>`sre` `finops` `llmops` `grafana`</sub> | 1 | Observability, LLMOps & FinOps | 2026-09 |
| [**tierdecay**](https://github.com/alebgl77/tierdecay)<br><sub>alebgl77</sub> | Per-repo learning layer for AI coding model routers: learns which task classes can safely run on a cheaper tier. Native for Claude Code, Codex, Antigravity · MCP server · zero deps.<br><sub>`agents-md` `ai-coding` `claude-code` `agent-skills`</sub> | 1 | AI Coding Agents & Skills | 2026-10 |
| [**design-md-viewer**](https://github.com/alebgl77/design-md-viewer)<br><sub>alebgl77</sub> | Client-side explorer that parses a design-system markdown file into browsable tokens, a health audit and code exports.<br><sub>`wcag` `react` `design-md` `tailwindcss`</sub> | 0 | Frontend, Design & Generative UI | 2026-09 |
| [**dsh-plugin-otel-genai**](https://github.com/alebgl77/dsh-plugin-otel-genai)<br><sub>alebgl77</sub> | OpenTelemetry GenAI metrics for DeepSeek Harness: token usage and step latency per provider and model, exported over OTLP for Grafana and Prometheus<br><sub>`llmops` `grafana` `opentelemetry` `dsh-plugin`</sub> | 0 | Observability, LLMOps & FinOps | 2026-09 |
| [**ftp-deploy-mcp**](https://github.com/alebgl77/ftp-deploy-mcp)<br><sub>alebgl77</sub> | MCP server to deploy, inspect and transfer files over FTP/FTPS/SFTP from AI coding agents. Local confinement, SFTP host-key pinning, verified staged promotion, read-only mode and dry runs. Bilingual EN/FR.<br><sub>`mcp` `mcp-tools` `mcp-server` `model-context-protocol`</sub> | 0 | MCP & Tool Use | 2026-09 |
| [**generative-engine-monitor**](https://github.com/alebgl77/generative-engine-monitor)<br><sub>alebgl77</sub> | Measure brand visibility in AI answers with explainable scoring, confidence intervals and zero-cost replay.<br><sub>`aeo` `geo` `ai-search` `perplexity`</sub> | 0 | Generative Search, GEO & LLMO | 2026-09 |
| [**harnessmeter**](https://github.com/alebgl77/harnessmeter)<br><sub>alebgl77</sub> | Offline profiler for AI agent instructions, skills, subagents and MCP schemas. No API keys or network.<br><sub>`claude-md` `claude-code` `agent-harness` `prompt-engineering`</sub> | 0 | AI Coding Agents & Skills | 2026-09 |
| [**open-fullscreenshot**](https://github.com/alebgl77/open-fullscreenshot)<br><sub>alebgl77</sub> | Full-page screen capture extension for Chrome (Manifest V3) — scroll-and-stitch full page, visible area, element or region. activeTab only, no host permissions, no network, no telemetry. | 0 | Automation, Browser Agents & Productivity | 2026-09 |
| [**open-shadow-ai**](https://github.com/alebgl77/open-shadow-ai)<br><sub>alebgl77</sub> | Self-hosted Shadow AI discovery and governance. Evidence-first visibility across network, endpoints, Active Directory and Entra ID.<br><sub>`shadow-ai` `ai-governance` `cybersecurity` `docker`</sub> | 0 | AI Security, Safety & Governance | 2026-10 |
| [**openspanguard**](https://github.com/alebgl77/openspanguard)<br><sub>alebgl77</sub> | Make AI quality observable. OpenTelemetry trace enrichment, Jev evaluation, streaming deduplication, and cohort quality alerts.<br><sub>`otlp` `llmops` `grafana` `prometheus`</sub> | 0 | Observability, LLMOps & FinOps | 2026-10 |
| [**promptor**](https://github.com/alebgl77/promptor)<br><sub>alebgl77</sub> | Architecte de prompts sur mesure — protocole itératif human-in-the-loop avec mémoire apprenante, pour ChatGPT, Claude, Gemini, Midjourney, Cursor et agents<br><sub>`meta-prompt` `prompt-engineering` `gemini` `chatgpt`</sub> | 0 | Prompt & Context Engineering | 2026-07 |

## Recently starred

| Project | What it does | Stars | Category | Last push |
|:--|:--|--:|:--|:--|
| [**jevgrep**](https://github.com/dzhng/jevgrep)<br><sub>dzhng</sub> | Find code by asking what it does. A CLI for coding agents that uses Jev to discover relevant files and source context.<br><sub>`codex` `claude-code` `coding-agents` `semantic-search`</sub> | 2.2k | AI Coding Agents & Skills | 2026-10 |
| [**vibeflow-os**](https://github.com/picmakpro/vibeflow-os)<br><sub>picmakpro</sub> | Modules VibeFlow distribués aux labs (consolidator, infrastructure-audit, validator) | 44 | Cloud, DevOps & Infrastructure | 2026-10 |
| [**claude-code-best-practice**](https://github.com/shanraisshan/claude-code-best-practice)<br><sub>shanraisshan</sub> | from vibe coding to agentic engineering - practice makes claude perfect<br><sub>`claude-code` `vibe-coding` `agentic-ai` `context-engineering`</sub> | 67.1k | AI Coding Agents & Skills | 2026-10 |
| [**pwneye**](https://github.com/Hackerest/pwneye)<br><sub>Hackerest</sub> | Your ONVIF and RTSP camera companion for discovering and hacking real-world security cameras 🎥<br><sub>`security` `pentesting` `security-tools` `cctv`</sub> | 339 | AI Security, Safety & Governance | 2026-09 |
| [**mimik**](https://github.com/westpoint-io/mimik)<br><sub>westpoint-io</sub> | 🪄 A browser extension that captures your workflow as you click and turns it into a step-by-step guide with annotated screenshots 📸<br><sub>`workflow` `productivity` `chrome-extension` `react`</sub> | 1.4k | Automation, Browser Agents & Productivity | 2026-09 |
| [**ZCode**](https://github.com/zai-org/ZCode)<br><sub>zai-org</sub> | Z.ai's coding agent harness. Powerful, intelligent, extensible. | 7.4k | AI Coding Agents & Skills | 2026-09 |
| [**reverse-skill**](https://github.com/zhaoxuya520/reverse-skill)<br><sub>zhaoxuya520</sub> | Reverse Engineering / Authorized Penetration Testing / Security Research Skill Router Pack AI-powered routing + On-demand toolchain bootstrapping + Self-evolving knowledge base  Supports Claude Code, Kiro, Cursor, Cline, and other AI coding clients 逆向/渗透/安全技能路由包 - AI 自动路由 + 按需自举工具链 + 自动进化经验库 \| 支持 Claude Code / Kiro / Cursor / Cline 等代码 AI 客户端 | 39.6k | AI Coding Agents & Skills | 2026-09 |
| [**TencentDB-Agent-Memory**](https://github.com/TencentCloud/TencentDB-Agent-Memory)<br><sub>TencentCloud</sub> | TencentDB Agent Memory is a team-level memory hub for AI Agents — turning conversations, docs, and code into four reusable memory assets (Chat Memory, Skill, LLM-Wiki, Code-Graph) that are governed, shared, and equipped across agents and frameworks.<br><sub>`memory` `long-term-memory` `embedding` `vector-search`</sub> | 27.7k | Agent Memory & Persistent Context | 2026-09 |
| [**artemis**](https://github.com/google/artemis)<br><sub>google</sub> | ARTEMIS turns natural-language instructions into reliable Android automation. It automates end-to-end workflows, captures logs, and integrates seamlessly with AI coding assistants such as Antigravity, Codex, and Claude Code.  It also achieves 99%+ success rate on AndroidWorld Benchmark.<br><sub>`google` `android` `testing` `ai-agents`</sub> | 10.9k | Automation, Browser Agents & Productivity | 2026-10 |
| [**awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering)<br><sub>ai-boost</sub> | Awesome list for AI agent harness engineering: tools, patterns, evals, memory, MCP, permissions, observability, and orchestration.<br><sub>`context-engineering` `harness-engineering` `awesome-list` `mcp`</sub> | 4.7k | Prompt & Context Engineering | 2026-10 |

## MCP & Tool Use

Model Context Protocol servers, clients, gateways and function-calling infrastructure.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**chrome-devtools-mcp**](https://github.com/ChromeDevTools/chrome-devtools-mcp)<br><sub>ChromeDevTools</sub> | Chrome DevTools for coding agents<br><sub>`mcp` `mcp-server` `puppeteer` `chrome`</sub> | 52.9k | TypeScript | 2026-10 |
| [**paperbanana**](https://github.com/llmsresearch/paperbanana)<br><sub>llmsresearch</sub> | Open source implementation and extension of Google Research’s PaperBanana for automated academic figures, diagrams, and research visuals, expanded to new domains like slide generation.<br><sub>`mcp` `mcp-server` `agentic-ai` `multiagent`</sub> | 2.4k | Python | 2026-09 |
| [**wordpress-mcp**](https://github.com/Automattic/wordpress-mcp)<br><sub>Automattic</sub> | **Archived.** WordPress MCP — This repository will be deprecated as stable releases of mcp-adapter become available. Please use https://github.com/WordPress/mcp-adapter for ongoing development and support. | 944 | PHP | 2026-09 |

## Agent Memory & Persistent Context

Long-term memory layers, persistent context across sessions and knowledge stores for agents.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**claude-mem**](https://github.com/thedotmack/claude-mem)<br><sub>thedotmack</sub> | Persistent Context Across Sessions for Every Agent –  Captures everything your agent does during sessions, compresses it with AI, and injects relevant context back into future sessions. Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More<br><sub>`mem0` `long-term-memory` `claude-code` `claude-skills`</sub> | 95.8k | TypeScript | 2026-10 |
| [**supermemory**](https://github.com/supermemoryai/supermemory)<br><sub>supermemoryai</sub> | Memory and context engine + app that is extremely fast, scalable, and can be run fully locally. The Memory API for the AI era.<br><sub>`memory` `agent-memory` `tailwindcss` `vite`</sub> | 31.1k | TypeScript | 2026-10 |
| [**agentmemory**](https://github.com/rohitg00/agentmemory)<br><sub>rohitg00</sub> | #1 Persistent memory for AI coding agents based on real-world benchmarks<br><sub>`memory` `codex` `copilot` `claude`</sub> | 29.1k | TypeScript | 2026-10 |
| [**TencentDB-Agent-Memory**](https://github.com/TencentCloud/TencentDB-Agent-Memory)<br><sub>TencentCloud</sub> | TencentDB Agent Memory is a team-level memory hub for AI Agents — turning conversations, docs, and code into four reusable memory assets (Chat Memory, Skill, LLM-Wiki, Code-Graph) that are governed, shared, and equipped across agents and frameworks.<br><sub>`memory` `long-term-memory` `embedding` `vector-search`</sub> | 27.7k | TypeScript | 2026-09 |
| [**memsearch**](https://github.com/zilliztech/memsearch)<br><sub>zilliztech</sub> | A persistent, unified memory layer for all your AI agents (e.g. Claude Code, Codex, DSH), backed by Markdown and Milvus.<br><sub>`memory` `agent-memory` `long-term-memory` `rag`</sub> | 2.7k | Python | 2026-09 |
| [**google-memorybank-plugin**](https://github.com/Shubhamsaboo/google-memorybank-plugin)<br><sub>Shubhamsaboo</sub> | Vertex AI Memory Bank Plugin for OpenClaw | 157 | TypeScript | 2026-09 |

## Observability, LLMOps & FinOps

Tracing, monitoring, cost tracking and operations for LLM applications and agents in production.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**grafana**](https://github.com/grafana/grafana)<br><sub>grafana</sub> | The open and composable observability and data visualization platform. Visualize metrics, logs, and traces from multiple sources like Prometheus, Loki, Elasticsearch, InfluxDB, Postgres and many more.<br><sub>`grafana` `monitoring` `prometheus` `data-visualization`</sub> | 77.1k | TypeScript | 2026-10 |
| [**loki**](https://github.com/grafana/loki)<br><sub>grafana</sub> | Like Prometheus, but for logs.<br><sub>`grafana` `prometheus` `loki` `logging`</sub> | 29k | Go | 2026-10 |
| [**librechat-prom-exporter**](https://github.com/rubentalstra/librechat-prom-exporter)<br><sub>rubentalstra</sub> | A lightweight Node.js service built with Express, Mongoose, and prom-client that collects metrics from your LibreChat MongoDB database and exposes them on a "/metrics" endpoint for Prometheus scraping. Easily integrate with Grafana dashboards for comprehensive monitoring and visualization.<br><sub>`prometheus` `librechat` `exporter`</sub> | 36 | MDX | 2026-10 |

## AI Security, Safety & Governance

Guardrails, prompt-injection defense, agent security scanning, privacy and AI governance or compliance.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**shannon**](https://github.com/KeygraphHQ/shannon)<br><sub>KeygraphHQ</sub> | Shannon is an AI pentester for web applications and APIs. It analyzes your source code, identifies attack vectors, and executes real exploits to prove vulnerabilities before they reach production.<br><sub>`appsec` `security` `pentesting` `ai-security`</sub> | 48.6k | TypeScript | 2026-10 |
| [**semgrep**](https://github.com/semgrep/semgrep)<br><sub>semgrep</sub> | Lightweight static analysis for many languages. Find bug variants with patterns that look like source code.<br><sub>`sast` `static-analysis` `c` `go`</sub> | 16.9k | C | 2026-10 |
| [**agentshield**](https://github.com/affaan-m/agentshield)<br><sub>affaan-m</sub> | AI agent security scanner. Detect vulnerabilities in agent configurations, MCP servers, and tool permissions. Available as CLI, GitHub Action, ECC plugin, and GitHub App integration. 🛡️<br><sub>`security` `mcp` `claude-code` `opus`</sub> | 1.2k | TypeScript | 2026-09 |
| [**pwneye**](https://github.com/Hackerest/pwneye)<br><sub>Hackerest</sub> | Your ONVIF and RTSP camera companion for discovering and hacking real-world security cameras 🎥<br><sub>`security` `pentesting` `security-tools` `cctv`</sub> | 339 | Python | 2026-09 |
| [**claude-security-audit**](https://github.com/VicKayro/claude-security-audit)<br><sub>VicKayro</sub> | Skill Claude Code pour audit de sécurité complet (OWASP Top 10, CWE/CVE, headers, auth, paywall, infra) | 80 |  | 2026-03 |

## Generative Search, GEO & LLMO

Visibility in AI answers: generative engine optimization, AI search monitoring and SEO for LLMs.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**claude-seo**](https://github.com/AgriciDaniel/claude-seo)<br><sub>AgriciDaniel</sub> | Universal SEO skill for Claude Code. 26 sub-skills + 19 sub-agents covering technical SEO, E-E-A-T, schema, GEO/AEO, agent readiness (Lighthouse Agentic Browsing, WebMCP, llms.txt), backlinks, local SEO, e-commerce, international SEO, Google APIs, and PDF/Excel reporting. 9 optional extensions, including DataForSEO, Firecrawl, Ahrefs and Matomo.<br><sub>`seo` `claude-code` `ai` `ai-seo`</sub> | 18.3k | Python | 2026-09 |
| [**Citatra**](https://github.com/Citatra/Citatra)<br><sub>Citatra</sub> | Citatra is an open-source platform for AEO/GEO. Designed for marketers and SEO professionals, it helps you monitor competitors, analyze backlinks, and gain actionable intelligence to optimize your visibility on AI search.<br><sub>`aeo` `geo` `ai` `ai-analytics`</sub> | 16 | TypeScript | 2026-02 |

## Prompt & Context Engineering

Prompt design and optimization, context engineering, structured outputs and instruction profiling.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**gsd-core**](https://github.com/open-gsd/gsd-core)<br><sub>open-gsd</sub> | Git. Ship. Done - Core<br><sub>`context-engineering` `claude-code` `meta-prompting` `spec-driven-development`</sub> | 10.1k | JavaScript | 2026-10 |
| [**awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering)<br><sub>ai-boost</sub> | Awesome list for AI agent harness engineering: tools, patterns, evals, memory, MCP, permissions, observability, and orchestration.<br><sub>`context-engineering` `harness-engineering` `awesome-list` `mcp`</sub> | 4.7k | Python | 2026-10 |

## AI Coding Agents & Skills

Coding agents, IDE copilots, agent skills, plugins and harness tooling for Claude Code, Codex, Cursor and peers.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**superpowers**](https://github.com/obra/superpowers)<br><sub>obra</sub> | An agentic skills framework & software development methodology that works.<br><sub>`skills` `coding` `ai` `obra`</sub> | 295k | Shell | 2026-09 |
| [**skills**](https://github.com/mattpocock/skills)<br><sub>mattpocock</sub> | Skills for Real Engineers. Straight from my .agents directory. | 275.6k | Shell | 2026-09 |
| [**ECC**](https://github.com/affaan-m/ECC)<br><sub>affaan-m</sub> | The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.<br><sub>`claude-code` `mcp` `productivity` `claude`</sub> | 272.5k | JavaScript | 2026-10 |
| [**spec-kit**](https://github.com/github/spec-kit)<br><sub>github</sub> | 💫 Toolkit to help you get started with SDD or any other process!<br><sub>`copilot` `ai` `prd` `spec`</sub> | 140k | Python | 2026-10 |
| [**gstack**](https://github.com/garrytan/gstack)<br><sub>garrytan</sub> | Use Garry Tan's exact Claude Code setup: 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA | 135k | TypeScript | 2026-10 |
| [**graphify**](https://github.com/Graphify-Labs/graphify)<br><sub>Graphify-Labs</sub> | Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill for Claude Code, Cursor, Codex, and Gemini CLI: local deterministic AST parsing, every edge explained, no vector store.<br><sub>`codex` `skills` `claude-code` `rag`</sub> | 123.6k | Python | 2026-10 |
| [**agent-skills**](https://github.com/addyosmani/agent-skills)<br><sub>addyosmani</sub> | Production-grade engineering skills for AI coding agents.<br><sub>`codex` `skills` `claude-code` `agent-skills`</sub> | 100.9k | JavaScript | 2026-10 |
| [**open-design**](https://github.com/nexu-io/open-design)<br><sub>nexu-io</sub> | 🎨 Best DeepSeek Harness Design Plugin. The open-source Claude Design alternative. 🖥️ Local-first desktop app. 🖼️ Your coding agent becomes the design engine: prototypes, landing pages, dashboards, slides, images & video — real files, HTML/PDF/PPTX/MP4 export. 🤖 Claude Code / Codex / Cursor / DeepSeek Harness / OpenCode & 20+ CLIs via BYOK.<br><sub>`vibe-coding` `agent-skills` `coding-agents` `design-systems`</sub> | 99.4k | TypeScript | 2026-10 |
| [**taste-skill**](https://github.com/Leonxlnx/taste-skill)<br><sub>Leonxlnx</sub> | Taste-Skill - gives your AI good taste. stops the AI from generating boring, generic slop<br><sub>`codex` `skill` `skills` `vibecoding`</sub> | 92.4k | JavaScript | 2026-09 |
| [**Agent-Reach**](https://github.com/Panniantong/Agent-Reach)<br><sub>Panniantong</sub> | Give your AI agent eyes to see the entire internet. Read & search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu — one CLI, zero API fees.<br><sub>`claude-code` `mcp` `ai-search` `cli`</sub> | 90.2k | Python | 2026-09 |
| [**awesome-claude-skills**](https://github.com/ComposioHQ/awesome-claude-skills)<br><sub>ComposioHQ</sub> | A curated list of awesome Claude Skills, resources, and tools for customizing Claude AI workflows<br><sub>`codex` `skill` `gemini-cli` `claude-code`</sub> | 76.4k | Python | 2026-09 |
| [**claude-code-best-practice**](https://github.com/shanraisshan/claude-code-best-practice)<br><sub>shanraisshan</sub> | from vibe coding to agentic engineering - practice makes claude perfect<br><sub>`claude-code` `vibe-coding` `agentic-ai` `context-engineering`</sub> | 67.1k | HTML | 2026-10 |
| [**awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code)<br><sub>hesreallyhim</sub> | A hand-picked collection of the finest of resources for the most awesome of agents, Claude Code, the undisputed champion of coding companions, from the unstoppable team at Anthropic PBC. A delectable showcase of top tier skills, ambidextrous agents, scintillating status lines, top notch developer tooling, and also we have plugins<br><sub>`claude-code` `agent-skills` `coding-agent` `coding-agents`</sub> | 55k | Python | 2026-10 |
| [**humanizer**](https://github.com/blader/humanizer)<br><sub>blader</sub> | Agent skill that removes signs of AI-generated writing from text<br><sub>`codex` `claude-code` `agent-skills` `prompt-engineering`</sub> | 53.8k | Python | 2026-09 |
| [**obsidian-skills**](https://github.com/kepano/obsidian-skills)<br><sub>kepano</sub> | Agent skills for Obsidian. Teach your agent to use Obsidian CLI and open formats including Markdown, Bases, JSON Canvas.<br><sub>`codex` `skills` `obsidian` `cli`</sub> | 49.1k |  | 2026-09 |
| [**herdr**](https://github.com/herdrdev/herdr)<br><sub>herdrdev</sub> | the runtime your coding agents live on<br><sub>`codex` `claude-code` `coding-agents` `cli`</sub> | 42.1k | Rust | 2026-10 |
| [**reverse-skill**](https://github.com/zhaoxuya520/reverse-skill)<br><sub>zhaoxuya520</sub> | Reverse Engineering / Authorized Penetration Testing / Security Research Skill Router Pack AI-powered routing + On-demand toolchain bootstrapping + Self-evolving knowledge base  Supports Claude Code, Kiro, Cursor, Cline, and other AI coding clients 逆向/渗透/安全技能路由包 - AI 自动路由 + 按需自举工具链 + 自动进化经验库 \| 支持 Claude Code / Kiro / Cursor / Cline 等代码 AI 客户端 | 39.6k | PowerShell | 2026-09 |
| [**openwiki**](https://github.com/langchain-ai/openwiki)<br><sub>langchain-ai</sub> | OpenWiki is a CLI that writes and maintains agent documentation for your codebase. | 17k | TypeScript | 2026-10 |
| [**OpenSpace**](https://github.com/HKUDS/OpenSpace)<br><sub>HKUDS</sub> | "OpenSpace: The Skill Management Layer for AI Agents" -- https://open-space.cloud/ | 7.7k | Python | 2026-08 |
| [**ZCode**](https://github.com/zai-org/ZCode)<br><sub>zai-org</sub> | Z.ai's coding agent harness. Powerful, intelligent, extensible. | 7.4k | TypeScript | 2026-09 |

<details><summary>4 more in AI Coding Agents & Skills</summary>

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**skills**](https://github.com/trailofbits/skills)<br><sub>trailofbits</sub> | Trail of Bits Claude Code skills for security research, vulnerability detection, and audit workflows<br><sub>`agent-skills`</sub> | 7.4k | Python | 2026-10 |
| [**tons-of-skills-marketplace**](https://github.com/jeremylongshore/tons-of-skills-marketplace)<br><sub>jeremylongshore</sub> | Model-agnostic agent-skills platform with a harness-free canonical layer, verified adapters, and the ccpi package manager. Explore at tonsofskills.com.<br><sub>`skills` `claude-code` `agent-skills` `mcp`</sub> | 2.8k | Python | 2026-10 |
| [**jevgrep**](https://github.com/dzhng/jevgrep)<br><sub>dzhng</sub> | Find code by asking what it does. A CLI for coding agents that uses Jev to discover relevant files and source context.<br><sub>`codex` `claude-code` `coding-agents` `semantic-search`</sub> | 2.2k | TypeScript | 2026-10 |
| [**helmor**](https://github.com/dohooo/helmor)<br><sub>dohooo</sub> | Open-source local workbench for multi-agent software development.<br><sub>`codex` `claude-code` `coding-agents` `multi-agent`</sub> | 1.3k | TypeScript | 2026-08 |

</details>

## Agent Frameworks & Orchestration

Frameworks and runtimes for single and multi-agent systems, planning, memory and orchestration.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**deepseek-harness**](https://github.com/deepseek-ai/deepseek-harness)<br><sub>deepseek-ai</sub> | DeepSeek Harness: Everything is a Plugin.<br><sub>`ai-agents` `dsh` `cordis` `dsh-plugin`</sub> | 243.1k | TypeScript | 2026-10 |
| [**deer-flow**](https://github.com/bytedance/deer-flow)<br><sub>bytedance</sub> | An open-source long-horizon SuperAgent harness that researches, codes, and creates. With the help of sandboxes, memories, tools, skill, subagents and message gateway, it handles different levels of tasks that could take minutes to hours.<br><sub>`agentic` `langchain` `langgraph` `multi-agent`</sub> | 83.4k | Python | 2026-10 |
| [**ruflo**](https://github.com/ruvnet/ruflo)<br><sub>ruvnet</sub> | 🌊 The original agent harness. Deploy intelligent multi-player swarms, coordinate autonomous workflows, and build conversational AI systems. Features adaptive memory, self-learning intelligence, federation, vector RAG integration, and native Claude Code / Codex / Hermes and many more Integrated<br><sub>`swarm` `agentic-ai` `multi-agent` `autonomous-agents`</sub> | 73.8k | TypeScript | 2026-10 |
| [**autogen**](https://github.com/microsoft/autogen)<br><sub>microsoft</sub> | A programming framework for agentic AI<br><sub>`agentic` `autogen` `llm-agent` `agents`</sub> | 61.2k | Python | 2026-04 |
| [**crewAI**](https://github.com/crewAIInc/crewAI)<br><sub>crewAIInc</sub> | Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks.<br><sub>`aiagentframework` `agents` `ai-agents` `ai`</sub> | 59.3k | Python | 2026-10 |
| [**multica**](https://github.com/multica-ai/multica)<br><sub>multica-ai</sub> | Make humans and AI agents work as one team — open-source and self-hostable. | 51.9k | Go | 2026-10 |
| [**nanobot**](https://github.com/HKUDS/nanobot)<br><sub>HKUDS</sub> | Ultra-lightweight, open-source, self-hosted personal AI agent framework in Python with WebUI, tools, memory, MCP, multi-agent workflows, automation, and chat apps<br><sub>`multi-agent` `agent-framework` `webui` `chatbot`</sub> | 48.8k | Python | 2026-10 |
| [**MiMo-Code**](https://github.com/XiaomiMiMo/MiMo-Code)<br><sub>XiaomiMiMo</sub> | MiMo Code: Where Models and Agents Co-Evolve<br><sub>`ai-agents` `ai` `cli` `mimo`</sub> | 13.6k | TypeScript | 2026-10 |
| [**swarms**](https://github.com/kyegomez/swarms)<br><sub>kyegomez</sub> | The Enterprise-Grade Multi-Agent Orchestration Framework. Website: https://swarms.ai<br><sub>`langchain` `agentic-ai` `multi-agent-systems` `prompt-engineering`</sub> | 7.2k | Python | 2026-10 |
| [**bigset-oss**](https://github.com/tinyfish-io/bigset-oss)<br><sub>tinyfish-io</sub> | Open-source BigSet — self-hostable live datasets populated by TinyFish web agents<br><sub>`bigset` `tinyfish` `open-source`</sub> | 1.7k | TypeScript | 2026-10 |
| [**n8n-openai-bridge**](https://github.com/sveneisenschmidt/n8n-openai-bridge)<br><sub>sveneisenschmidt</sub> | OpenAI-compatible API middleware for n8n workflows. Use your n8n agents and workflows as OpenAI models in any OpenAI-compatible client. | 131 | JavaScript | 2026-03 |

## Inference, Serving & Model Routing

Local and production inference engines, quantization, AI gateways and model routers.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**llama.cpp**](https://github.com/ggml-org/llama.cpp)<br><sub>ggml-org</sub> | LLM inference in C/C++<br><sub>`ggml`</sub> | 130.3k | C++ | 2026-10 |
| [**litellm**](https://github.com/BerriAI/litellm)<br><sub>BerriAI</sub> | The fastest, litest AI Gateway. Rust core with Python SDK. Call 100+ LLM APIs in OpenAI (or native) format with cost tracking, guardrails, load balancing, and logging [Bedrock, Azure, OpenAI, Anthropic, OpenAI, VertexAI, vLLM, Nvidia NIM]<br><sub>`gateway` `litellm` `ai-gateway` `llm-gateway`</sub> | 60.1k | Python | 2026-10 |

## Models, Training & Fine-tuning

Foundation models, fine-tuning, distillation, reinforcement learning, datasets and ML frameworks.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**kimi-k3-in-c**](https://github.com/FareedKhan-dev/kimi-k3-in-c)<br><sub>FareedKhan-dev</sub> | A 2.78-trillion-parameter Kimi K3 running inference on a single CPU in 8.24 GB of RAM. Portable C99: no BLAS, no framework, no GPU.<br><sub>`transformer` `deep-learning` `machine-learning` `quantization`</sub> | 8.9k | C | 2026-10 |

## Vision, Voice & Generative Media

Speech, text-to-speech, OCR, computer vision, image and video generation and multimodal models.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**Deep-Live-Cam**](https://github.com/hacksider/Deep-Live-Cam)<br><sub>hacksider</sub> | real time face swap and one-click video deepfake with only a single image<br><sub>`deepfake` `ai` `gan` `webcam`</sub> | 96.9k | Python | 2026-09 |
| [**meetily**](https://github.com/Zackriya-Solutions/meetily)<br><sub>Zackriya-Solutions</sub> | Privacy first, AI meeting assistant with 4x faster Parakeet/Whisper live transcription, speaker diarization, and Ollama summarization built on Rust. 100% local processing. no cloud required. Meetily (Meetly Ai - https://meetily.ai) is the #1 Self-hosted, Open-source Ai meeting note taker for macOS & Windows. Understand How to write meeting minutes<br><sub>`whisper` `meeting-notes` `transcription` `speech-to-text`</sub> | 31.4k | Rust | 2026-09 |
| [**vexa**](https://github.com/Vexa-ai/vexa)<br><sub>Vexa-ai</sub> | Open-source meeting transcription API for Google Meet, Microsoft Teams & Zoom. Auto-join bots, real-time WebSocket transcripts, MCP server for AI agents. Self-host or use hosted SaaS.<br><sub>`meeting-notes` `transcription` `speech-to-text` `mcp`</sub> | 2.9k | Python | 2026-10 |

## Data Engineering, Scraping & Analytics

Pipelines, web crawling for LLMs, text-to-SQL, warehouses and analytics tooling.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**Scrapling**](https://github.com/D4Vinci/Scrapling)<br><sub>D4Vinci</sub> | 🕷️ An adaptive Web Scraping framework that handles everything from a single request to a full-scale crawl! Don't be shy, join here: https://discord.gg/EMgGbDceNQ and follow here for daily tips and tricks: https://x.com/Scrapling_dev<br><sub>`crawler` `scraping` `web-scraping` `mcp`</sub> | 85.5k | Python | 2026-10 |
| [**awesome-web-scraping**](https://github.com/lorien/awesome-web-scraping)<br><sub>lorien</sub> | List of libraries, tools and APIs for web scraping and data processing.<br><sub>`crawler` `scraping` `web-scraping` `spider`</sub> | 8.2k | JavaScript | 2026-09 |

## Automation, Browser Agents & Productivity

Workflow automation, browser and computer-use agents, extensions and everyday productivity tools.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**obscura**](https://github.com/h4ckf0r0day/obscura)<br><sub>h4ckf0r0day</sub> | The headless browser for AI agents and web scraping<br><sub>`puppeteer` `playwright` `browser-automation` `cdp`</sub> | 28.3k | Rust | 2026-10 |
| [**obsidian-releases**](https://github.com/obsidianmd/obsidian-releases)<br><sub>obsidianmd</sub> | Community plugins list, theme list, and releases of Obsidian.<br><sub>`obsidian` `obsidian-md` `md` `bases`</sub> | 22k |  | 2026-10 |
| [**artemis**](https://github.com/google/artemis)<br><sub>google</sub> | ARTEMIS turns natural-language instructions into reliable Android automation. It automates end-to-end workflows, captures logs, and integrates seamlessly with AI coding assistants such as Antigravity, Codex, and Claude Code.  It also achieves 99%+ success rate on AndroidWorld Benchmark.<br><sub>`google` `android` `testing` `ai-agents`</sub> | 10.9k | Python | 2026-10 |
| [**n8n-skills**](https://github.com/czlonkowski/n8n-skills)<br><sub>czlonkowski</sub> | n8n skillset for Claude Code to build flawless n8n workflows<br><sub>`n8n` `workflow-automation` `ai-agents`</sub> | 6.4k | Shell | 2026-09 |
| [**mimik**](https://github.com/westpoint-io/mimik)<br><sub>westpoint-io</sub> | 🪄 A browser extension that captures your workflow as you click and turns it into a step-by-step guide with annotated screenshots 📸<br><sub>`workflow` `productivity` `chrome-extension` `react`</sub> | 1.4k | TypeScript | 2026-09 |
| [**awesome-workflow-automation**](https://github.com/dariubs/awesome-workflow-automation)<br><sub>dariubs</sub> | A curated list of Workflow Automation  Software, Engines and Tools<br><sub>`n8n` `zapier` `workflow` `workflow-automation`</sub> | 1.2k |  | 2026-04 |

## Frontend, Design & Generative UI

Design systems, UI components, design taste for AI agents and generative interfaces.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**payload**](https://github.com/payloadcms/payload)<br><sub>payloadcms</sub> | Payload is the open-source, fullstack Next.js framework, giving you instant backend superpowers. Get a full TypeScript backend and admin panel instantly. Use Payload as a headless CMS or for building powerful applications.<br><sub>`react` `nextjs` `mongodb` `typescript`</sub> | 45.1k | TypeScript | 2026-10 |
| [**design-extract**](https://github.com/Manavarya09/design-extract)<br><sub>Manavarya09</sub> | Extract any website's complete design system with one command. DTCG tokens, semantic+primitive+composite, MCP server for Claude Code/Cursor/Windsurf, multi-platform emitters (iOS SwiftUI, Android Compose, Flutter, WordPress), Tailwind v4, Figma variables, shadcn/ui, CSS health audit, WCAG remediation, Chrome extension. MIT, Playwright, Node 20+.<br><sub>`css` `figma` `tailwind` `accessibility`</sub> | 4.2k | HTML | 2026-09 |

## Cloud, DevOps & Infrastructure

Deployment, containers, CI/CD and cloud infrastructure for shipping AI systems.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**neon**](https://github.com/neondatabase/neon)<br><sub>neondatabase</sub> | Neon: Serverless Postgres. We separated storage and compute to offer autoscaling, code-like database branching, and scale to zero.<br><sub>`serverless` `rust` `database` `postgres`</sub> | 23.2k | Rust | 2026-08 |
| [**OpenSandbox**](https://github.com/opensandbox-group/OpenSandbox)<br><sub>opensandbox-group</sub> | Secure, Fast, and Extensible Sandbox runtime for AI agents.<br><sub>`kubernetes` `ai` `sandbox` `ai-agent`</sub> | 15.7k | Python | 2026-10 |
| [**vibeflow-os**](https://github.com/picmakpro/vibeflow-os)<br><sub>picmakpro</sub> | Modules VibeFlow distribués aux labs (consolidator, infrastructure-audit, validator) | 44 | Shell | 2026-10 |

## AI Apps & Chat Interfaces

End-user AI applications, chat UIs, assistants and business tools built on LLMs.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**odysseus**](https://github.com/odysseus-dev/odysseus)<br><sub>odysseus-dev</sub> | Self-hosted AI workspace. | 89.2k | Python | 2026-10 |
| [**LibreChat**](https://github.com/LibreChat-AI/LibreChat)<br><sub>LibreChat-AI</sub> | Enhanced ChatGPT Clone: Features Agents, MCP, Skills, DeepSeek, Anthropic, AWS, OpenAI, Responses API, Azure, Groq, o1, GPT-5, Mistral, OpenRouter, Vertex AI, Gemini, Artifacts, AI model switching, message search, Code Interpreter, langchain, DALL-E-3, OpenAPI Actions, Functions, Secure Multi-User Auth, Presets, open-source for self-hosting. Active<br><sub>`webui` `librechat` `aws` `azure`</sub> | 45.2k | TypeScript | 2026-10 |
| [**cheating-daddy**](https://github.com/sohzm/cheating-daddy)<br><sub>sohzm</sub> | a free and opensource app that lets you gain an unfair advantage | 5.6k | JavaScript | 2026-07 |
| [**AzuraCast**](https://github.com/AzuraCast/AzuraCast)<br><sub>AzuraCast</sub> | A self-hosted web radio management suite, including turnkey installer tools for the full radio software stack and a modern, easy-to-use web app to manage your stations.<br><sub>`radio` `icecast` `station` `webcast`</sub> | 4.1k | PHP | 2026-10 |

## Learning, Papers & Awesome Lists

Curated lists, courses, cookbooks, tutorials and research references.

| Project | What it does | Stars | Language | Last push |
|:--|:--|--:|:--|:--|
| [**claude-cookbooks**](https://github.com/anthropics/claude-cookbooks)<br><sub>anthropics</sub> | A collection of notebooks/recipes showcasing some fun and effective ways of using Claude. | 53.2k | Jupyter Notebook | 2026-09 |
| [**awesome-hermes-agent**](https://github.com/0xNyk/awesome-hermes-agent)<br><sub>0xNyk</sub> | Independent directory of useful skills, plugins, memory providers, tools, surfaces, and guides for Nous Research's open-source Hermes Agent.<br><sub>`awesome` `awesome-list` `skills` `agent-skills`</sub> | 5.8k |  | 2026-09 |
| [**awesome-claude-fable-5-prompt-vault**](https://github.com/thenicolas1894/awesome-claude-fable-5-prompt-vault)<br><sub>thenicolas1894</sub> | Ultimate Claude Fable 5 Guide 2026: Use Cases, Integrations & Benchmarks<br><sub>`awesome-list` `prompt-engineering` `benchmarks` `llm`</sub> | 141 | HTML | 2026-10 |

## How it works

1. A scheduled GitHub Action fetches every public star and public original repository of [@alebgl77](https://github.com/alebgl77) through the GitHub API.
2. Each repository is scored against a taxonomy of AI-engineering categories using its topics, name and description. Topics weigh most because maintainers curate them.
3. Daily snapshots of star counts give a momentum signal (stars gained over about 30 days).
4. This README, a JSON dataset and the interactive explorer are regenerated and published.

The taxonomy, weights and manual overrides live in [`config.toml`](config.toml). The generator is a single dependency-free Python file: [`scripts/build.py`](scripts/build.py). Fork it, change one line (`user`), and get the same list for your own stars.

### Use it for your own stars

1. [Fork this repository](https://github.com/alebgl77/awesome-ai-architect/fork) (or copy `config.toml`, `scripts/`, `site/` and `.github/workflows/awesome.yml`).
2. Set `user`, `repo` and `site_url` in `config.toml`, and empty `[overrides]`.
3. In Settings > Pages, set Source to **GitHub Actions**.
4. Run the workflow once from the Actions tab. It then refreshes every day on its own.

No secrets, no API keys and no dependencies: the default `GITHUB_TOKEN` reads public stars.

## Suggest a project

This list mirrors what one practitioner actually uses and follows. Know a project that belongs here? [Open a suggestion](https://github.com/alebgl77/awesome-ai-architect/issues/new?template=suggest.yml). Accepted suggestions get starred, then classified on the next run.

## License

Code: [MIT](LICENSE). List content: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Project descriptions belong to their respective authors.
