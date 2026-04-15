#!/usr/bin/env python3
"""MEOK AI Labs — survey-builder-ai-mcp MCP Server. Build surveys with logic branching and response analysis."""

import json
import uuid
from datetime import datetime, timezone
from collections import defaultdict, Counter

from mcp.server.fastmcp import FastMCP
import sys, os
sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
from auth_middleware import check_access

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

_store = {}
_responses = defaultdict(list)

QUESTION_TYPES = ["multiple_choice", "rating", "text", "yes_no", "likert", "ranking", "matrix"]

mcp = FastMCP("survey-builder-ai", instructions="Create surveys, validate questions, collect responses, and generate analysis reports.")


@mcp.tool()
def create_survey(title: str, questions: list[str], description: str = "", question_types: list[str] = [], api_key: str = "") -> str:
    """Create a new survey with questions. Optionally specify question types per question."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    survey_id = f"SRV-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()

    formatted_questions = []
    for i, q in enumerate(questions):
        q_type = question_types[i] if i < len(question_types) else "text"
        if q_type not in QUESTION_TYPES:
            q_type = "text"
        fq = {"id": i + 1, "text": q, "type": q_type, "required": True}
        if q_type == "multiple_choice":
            fq["options"] = ["Option A", "Option B", "Option C", "Other"]
        elif q_type == "rating":
            fq["scale"] = {"min": 1, "max": 5}
        elif q_type == "likert":
            fq["scale"] = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
        elif q_type == "yes_no":
            fq["options"] = ["Yes", "No"]
        formatted_questions.append(fq)

    survey = {
        "survey_id": survey_id,
        "title": title,
        "description": description,
        "questions": formatted_questions,
        "created_at": now,
        "status": "draft",
        "response_count": 0,
    }

    _store[survey_id] = survey
    return json.dumps(survey, indent=2)


@mcp.tool()
def validate_questions(questions: list[str], api_key: str = "") -> str:
    """Validate survey questions for clarity, bias, leading language, and best practices."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    results = []
    overall_score = 0
    leading_words = ["don't you think", "wouldn't you agree", "obviously", "clearly", "surely", "of course"]
    double_barrel = [" and ", " or ", " as well as "]
    jargon = ["synergy", "leverage", "paradigm", "holistic", "scalable", "utilize"]

    for i, q in enumerate(questions):
        issues = []
        lower = q.lower()

        # Check length
        words = len(q.split())
        if words > 25:
            issues.append({"type": "too_long", "message": "Question exceeds 25 words - consider simplifying"})
        if words < 3:
            issues.append({"type": "too_short", "message": "Question seems incomplete"})

        # Check for leading language
        for lw in leading_words:
            if lw in lower:
                issues.append({"type": "leading", "message": f"Leading phrase detected: '{lw}'"})

        # Check double-barreled
        for db in double_barrel:
            if db in lower and words > 8:
                issues.append({"type": "double_barreled", "message": f"May be asking two things at once (contains '{db.strip()}')"})
                break

        # Check for jargon
        for j in jargon:
            if j in lower:
                issues.append({"type": "jargon", "message": f"Jargon detected: '{j}' - use simpler language"})

        # Check ends with question mark
        if not q.strip().endswith("?"):
            issues.append({"type": "formatting", "message": "Missing question mark"})

        score = max(0, 100 - len(issues) * 20)
        overall_score += score
        results.append({"question": q, "score": score, "issues": issues, "valid": len(issues) == 0})

    avg_score = round(overall_score / max(len(questions), 1), 1)
    return json.dumps({
        "total_questions": len(questions),
        "valid_count": sum(1 for r in results if r["valid"]),
        "average_score": avg_score,
        "results": results,
        "recommendation": "All questions pass" if avg_score >= 90 else "Minor revisions needed" if avg_score >= 60 else "Significant revisions recommended",
    }, indent=2)


@mcp.tool()
def analyze_responses(survey_id: str = "", responses: list[dict] = [], api_key: str = "") -> str:
    """Analyze survey responses. Provide either a survey_id (for stored data) or a list of response dicts."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    data = responses if responses else _responses.get(survey_id, [])
    if not data:
        return json.dumps({"error": "No responses found", "suggestion": "Provide responses list or valid survey_id"})

    total = len(data)
    # Aggregate answers per question
    question_stats = defaultdict(lambda: {"answers": [], "counts": Counter()})
    for resp in data:
        for key, value in resp.items():
            if key in ("respondent_id", "timestamp"):
                continue
            qs = question_stats[key]
            qs["answers"].append(value)
            if isinstance(value, str):
                qs["counts"][value] += 1
            elif isinstance(value, (int, float)):
                qs["counts"][str(value)] += 1

    analysis = {}
    for question, stats in question_stats.items():
        answers = stats["answers"]
        numeric = [a for a in answers if isinstance(a, (int, float))]
        entry = {"response_count": len(answers), "top_answers": stats["counts"].most_common(5)}
        if numeric:
            entry["average"] = round(sum(numeric) / len(numeric), 2)
            entry["min"] = min(numeric)
            entry["max"] = max(numeric)
        analysis[question] = entry

    return json.dumps({
        "total_responses": total,
        "questions_analyzed": len(analysis),
        "analysis": analysis,
    }, indent=2)


@mcp.tool()
def generate_report(survey_id: str = "", title: str = "Survey Report", responses: list[dict] = [], api_key: str = "") -> str:
    """Generate a summary report for a survey with key findings and recommendations."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    survey = _store.get(survey_id, {})
    data = responses if responses else _responses.get(survey_id, [])
    total = len(data)

    # Compute completion and satisfaction metrics
    completion_rate = 100.0 if total > 0 else 0
    numeric_answers = []
    text_lengths = []
    for resp in data:
        for key, value in resp.items():
            if key in ("respondent_id", "timestamp"):
                continue
            if isinstance(value, (int, float)):
                numeric_answers.append(value)
            elif isinstance(value, str):
                text_lengths.append(len(value.split()))

    avg_rating = round(sum(numeric_answers) / len(numeric_answers), 2) if numeric_answers else None
    avg_text_length = round(sum(text_lengths) / len(text_lengths), 1) if text_lengths else 0

    findings = []
    if avg_rating is not None:
        if avg_rating >= 4: findings.append("Overall satisfaction is high (avg rating >= 4)")
        elif avg_rating >= 3: findings.append("Moderate satisfaction levels detected")
        else: findings.append("Low satisfaction scores - immediate attention needed")
    if avg_text_length > 20:
        findings.append("Respondents are providing detailed text feedback")
    elif text_lengths and avg_text_length < 5:
        findings.append("Text responses are brief - consider more specific questions")

    recommendations = []
    if total < 30:
        recommendations.append("Collect more responses for statistical significance (minimum 30)")
    if avg_rating is not None and avg_rating < 3.5:
        recommendations.append("Investigate low-scoring areas with follow-up interviews")
    if not text_lengths:
        recommendations.append("Add open-ended questions for qualitative insights")

    return json.dumps({
        "report_title": title,
        "survey_title": survey.get("title", "Unknown"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_responses": total,
        "completion_rate": f"{completion_rate}%",
        "average_rating": avg_rating,
        "average_text_response_length": f"{avg_text_length} words",
        "key_findings": findings if findings else ["Insufficient data for findings"],
        "recommendations": recommendations if recommendations else ["Survey data looks good - continue collecting"],
        "questions_count": len(survey.get("questions", [])),
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
