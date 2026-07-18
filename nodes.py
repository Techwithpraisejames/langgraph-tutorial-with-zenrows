import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_zenrows import ZenRowsUniversalScraper

from state import ResearchState

load_dotenv()

# initialize the scraper and model
scraper = ZenRowsUniversalScraper()
llm = ChatOpenAI(model="gpt-4o-mini")

def scrape_node(state: ResearchState) -> ResearchState:
    results = []

    for url in state["urls"]:
        content = scraper.invoke(
            {
                "url": url,
                "js_render": True,
                "premium_proxy": True,
                "response_type": "markdown",
            }
        )

        results.append(content)

    status = (
        "blocked"
        if any(is_blocked(content) for content in results)
        else "ok"
    )

    return {
        **state,
        "results": results,
        "status": status,
    }

BLOCK_SIGNALS = [
    "Checking your browser",
    "Enable JavaScript and cookies to continue",
    "Verify you are human",
]



def is_blocked(content: str) -> bool:
    # empty responses are unusable
    if not content.strip():
        return True

    # common challenge page signals
    return any(signal in content for signal in BLOCK_SIGNALS)


def retry_node(state: ResearchState) -> ResearchState:
    results = list(state["results"])

    for index, content in enumerate(results):
        if not is_blocked(content):
            continue

        retried_content = scraper.invoke(
            {
                "url": state["urls"][index],
                "js_render": True,
                "premium_proxy": True,
                "proxy_country": "us",
                "response_type": "markdown",
            }
        )

        # log failed retries before advancing
        if is_blocked(retried_content):
            print(
                f"Retry failed for {state['urls'][index]}. "
                "Advancing with blocked content."
            )

        results[index] = retried_content

    status = (
        "blocked"
        if any(is_blocked(content) for content in results)
        else "ok"
    )

    return {
        **state,
        "results": results,
        "status": status,
        "retry_count": state["retry_count"] + 1,
    }

def check_retrieval(state: ResearchState) -> str:
    if state["status"] == "blocked" and state["retry_count"] < 1:
        return "retry"

    return "continue"

def extract_node(state: ResearchState) -> ResearchState:
    extracted = []

    for i, content in enumerate(state["results"]):
        response = llm.invoke(
            f"""
Extract the following fields from this article.

Return valid JSON only. No markdown fences, no preamble.

{{
  "headline": "...",
  "source": "...",
  "date": "...",
  "summary": "..."
}}

Article:

{content[:4000]}
"""
        )

        cleaned = (
            response.content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            extracted.append(json.loads(cleaned))
        except json.JSONDecodeError:
            print(
                f"JSON parse failed for article {i}. "
                f"Raw response:\n{cleaned[:300]}"
            )
            extracted.append({
                "headline": "Parse error",
                "source": state["urls"][i] if i < len(state["urls"]) else "unknown",
                "date": "",
                "summary": "Extraction failed. The model returned malformed JSON.",
            })

    return {
        **state,
        "extracted": extracted,
    }

def synthesize_node(state: ResearchState) -> ResearchState:
    response = llm.invoke(
        f"""
Write a concise news briefing.

Requirements:
- One bullet per story
- Preserve the key facts
- Keep each bullet under 40 words

Articles:

{json.dumps(state["extracted"], indent=2)}
"""
    )

    return {
        **state,
        "briefing": response.content,
    }