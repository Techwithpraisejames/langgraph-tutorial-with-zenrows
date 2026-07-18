from typing import TypedDict


class ResearchState(TypedDict):
    urls: list[str]
    results: list[str]
    extracted: list[dict]
    briefing: str
    current_url: str
    status: str
    retry_count: int

