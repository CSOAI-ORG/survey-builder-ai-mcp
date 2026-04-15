# Survey Builder Ai

> By [MEOK AI Labs](https://meok.ai) — Create surveys, validate questions, collect responses, and generate analysis reports.

MEOK AI Labs — survey-builder-ai-mcp MCP Server. Build surveys with logic branching and response analysis.

## Installation

```bash
pip install survey-builder-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install survey-builder-ai-mcp
```

## Tools

### `create_survey`
Create a new survey with questions. Optionally specify question types per question.

**Parameters:**
- `title` (str)
- `questions` (str)
- `description` (str)
- `question_types` (str)

### `validate_questions`
Validate survey questions for clarity, bias, leading language, and best practices.

**Parameters:**
- `questions` (str)

### `analyze_responses`
Analyze survey responses. Provide either a survey_id (for stored data) or a list of response dicts.

**Parameters:**
- `survey_id` (str)
- `responses` (str)

### `generate_report`
Generate a summary report for a survey with key findings and recommendations.

**Parameters:**
- `survey_id` (str)
- `title` (str)
- `responses` (str)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/survey-builder-ai-mcp](https://github.com/CSOAI-ORG/survey-builder-ai-mcp)
- **PyPI**: [pypi.org/project/survey-builder-ai-mcp](https://pypi.org/project/survey-builder-ai-mcp/)

## License

MIT — MEOK AI Labs
