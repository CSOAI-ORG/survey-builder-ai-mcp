<!-- mcp-name: io.github.CSOAI-ORG/survey-builder-ai-mcp -->
[![MCP Scorecard: 86/100](https://img.shields.io/badge/proofof.ai-86%2F100-5b21b6)](https://proofof.ai/scorecard/survey-builder-ai-mcp.html)

# Survey Builder Ai MCP

[![MEOK AI Labs](https://img.shields.io/badge/MEOK-AI%20Labs-667eea)](https://meok.ai)
[![GSPC](https://img.shields.io/badge/GSPC-UNMEASURED-9ca3af)](https://councilof.ai/api/gspc)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Install-3775a9)](https://pypi.org/project/survey_builder_ai_mcp/)
mcp-name: io.github.CSOAI-ORG/survey-builder-ai-mcp

# Survey Builder Ai

[![PyPI](https://img.shields.io/pypi/v/survey-builder-ai-mcp)](https://pypi.org/project/survey-builder-ai-mcp/) [![Python](https://img.shields.io/pypi/pyversions/survey-builder-ai-mcp)](https://pypi.org/project/survey-builder-ai-mcp/)


> By [MEOK AI Labs](https://meok.ai) — Create surveys, validate questions, collect responses, and generate analysis reports.

> Create surveys, validate questions, collect responses, and generate analysis reports

Create surveys, validate questions, collect responses, and generate analysis reports.

---

## 🚀 Quick Start

```bash
# Install via pip
pip install survey_builder_ai_mcp

# Or install via Smithery
npx -y @smithery/cli@latest install survey-builder-ai-mcp --client claude
```

## ✨ Features

- MCP protocol compliant
- Easy installation
- Well-documented API
- Production-ready
- Active maintenance

## 📖 Documentation

- [Full Documentation](https://docs.meok.ai/survey-builder-ai-mcp)
- [API Reference](https://api.meok.ai)
- [EU AI Act Compliance Guide](https://councilof.ai/compliance)

## 🛡️ Compliance

This MCP server is built with **EU AI Act compliance** built-in:

- ✅ Article 9 — Risk Management System
- ✅ Article 13 — Transparency & Instructions for Use
- ✅ Article 15 — Bias Detection & Testing
- ✅ Article 26 — FRIA Support (where applicable)
- ✅ Article 50 — AI Content Watermarking (where applicable)

Need help getting compliant? **[Book a free 15-min diagnostic →](https://cal.com/csoai/august-audit)**

## How MEOK charges

MEOK has no subscriptions and no tiers. You pay per job, and only when the agreed artifact has been delivered to you. There is no public price list. See <https://meok.ai/pricing>.

This repository's source is MIT-licensed and free to self-host.

## 🤝 Part of the MEOK Ecosystem

This server is part of the **[MEOK AI Labs](https://meok.ai)** ecosystem — 300+ MCP servers for sovereign AI governance.

| Domain | Purpose |
|--------|---------|
| [councilof.ai](https://councilof.ai) | EU AI Act compliance marketplace |
| [safetyof.ai](https://safetyof.ai) | AI safety & monitoring |
| [meok.ai](https://meok.ai) | Sovereign AI platform |
| [cobolbridge.ai](https://cobolbridge.ai) | Legacy modernization |

## 📜 License

MIT © [CSOAI-ORG](https://github.com/CSOAI-ORG)

---

<p align="center">
  <sub>Built with 💜 by <a href="https://meok.ai">MEOK AI Labs</a> · UK Companies House 16939677</sub>
</p>
MIT — MEOK AI Labs

<!-- meok-moat-footer-v1 -->
---

## Pairs with MEOK Governance Suite

Build something that touches users? You need compliance. MEOK ships 38 governance MCPs that drop in alongside this tool — EU AI Act, DORA, NIS2, CRA, GDPR, ISO 42001, FDA SaMD, MDR, Basel, MiFID II, MiCA, COPPA, and more.

```bash
# One-shot install of the governance pack
npx meok-setup --pack governance
```


→ Full catalogue: [councilof.ai](https://councilof.ai)
→ MEOK AI Labs: [meok.ai](https://meok.ai)



## Configuration

Add to your `claude_desktop_config.json` (Claude Desktop) or your MCP client config:

```json
{
  "mcpServers": {
    "survey-builder-ai-mcp": {
      "command": "uvx",
      "args": ["survey-builder-ai-mcp"]
    }
  }
}
```

Or: `pip install survey-builder-ai-mcp` then run the `survey-builder-ai-mcp` command (stdio transport).

## Examples

Once configured, ask your assistant, for example:
- "Use `create_survey` to …"
- "Use `validate_questions` to …"
- "Use `analyze_responses` to …"
