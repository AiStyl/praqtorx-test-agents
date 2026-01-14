# PRAQTOR X Test Agents Repository

This repository contains sample AI agents across multiple frameworks for testing PRAQTOR X's discovery and risk assessment capabilities.

## ⚠️ WARNING

**These agents are intentionally designed with various security risks for testing purposes. DO NOT deploy in production.**

## Agent Inventory

### LangChain Agents

| Agent | Risk Level | Capabilities |
|-------|------------|--------------|
| `data_extraction_agent.py` | 🔴 CRITICAL | Shell exec, file write, HTTP, DB query, webhooks |
| `research_assistant.py` | 🟠 HIGH | Web search, external APIs, S3 storage |
| `faq_chatbot.py` | 🟢 LOW | Read-only FAQ lookup, product info |

### CrewAI Multi-Agent Systems

| Crew | Risk Level | Capabilities |
|------|------------|--------------|
| `financial_crew.py` | 🔴 CRITICAL | Trade execution, fund transfers, portfolio access |
| `content_crew.py` | 🟡 MEDIUM | Web research, content publishing |

### AutoGen Agents

| Agent | Risk Level | Capabilities |
|-------|------------|--------------|
| `code_assistant.py` | 🟠 HIGH | Code generation, arbitrary code execution |

### MCP Server Configurations

| Config | Risk Level | Servers |
|--------|------------|---------|
| `claude_desktop_config.json` | 🔴 CRITICAL | Filesystem, shell, database, secrets |
| `safe_config.json` | 🟢 LOW | Weather, calculator, docs (read-only) |

## Risk Scoring Criteria

PRAQTOR X evaluates agents based on:

- **Shell/Code Execution** - Can run arbitrary commands (+40 risk)
- **File System Access** - Can read/write files (+25 risk)
- **External Network** - Can make HTTP requests (+20 risk)
- **Database Access** - Can query/modify data (+30 risk)
- **Secrets Access** - Can access credentials (+35 risk)
- **Financial Operations** - Can move money (+50 risk)

## Usage

This repo is designed to be scanned by PRAQTOR X:

1. Connect your GitHub account to PRAQTOR X
2. Select this repository
3. Click "Scan" to discover agents
4. Review risk assessments in the Agent Matrix

## License

MIT - For testing purposes only.
