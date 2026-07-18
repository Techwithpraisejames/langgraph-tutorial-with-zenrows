# LangGraph Tutorial with ZenRows

A [LangGraph](https://github.com/langchain-ai/langgraph) pipeline that scrapes news articles with [ZenRows](https://www.zenrows.com/), extracts structured fields with an LLM, and synthesizes a short briefing.

## How it works

The graph (`graph.py`) wires together four nodes (`nodes.py`):

1. **scrape** — fetches each URL with `ZenRowsUniversalScraper` (JS rendering + premium proxy).
2. **retry** — if a scrape looks blocked (bot-check page, empty response), retries once with a US proxy.
3. **extract** — asks `gpt-4o-mini` to pull `headline`, `source`, `date`, and `summary` from each article as JSON.
4. **synthesize** — asks the LLM to turn the extracted articles into a short bullet-point briefing.

```
scrape --(blocked?)--> retry --> extract --> synthesize --> END
   \_________________(ok)_______/
```

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with:

```
ZENROWS_API_KEY=your_zenrows_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Run

```bash
python graph.py
```

This scrapes a hardcoded list of URLs (edit the `urls` list in `graph.py` to change targets), prints the extracted fields, and prints the final briefing.
