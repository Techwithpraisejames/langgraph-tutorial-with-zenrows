from langgraph.graph import StateGraph
from langgraph.graph import END

from state import ResearchState


from nodes import (
    scrape_node,
    retry_node,
    check_retrieval,
    extract_node,
    synthesize_node,
)

graph = StateGraph(ResearchState)

# register nodes
graph.add_node("scrape", scrape_node)
graph.add_node("retry", retry_node)
graph.add_node("extract", extract_node)
graph.add_node("synthesize", synthesize_node)

# define entry point 
graph.set_entry_point("scrape")

# route blocked retrievals through retry
graph.add_conditional_edges(
    "scrape",
    check_retrieval,
    {
        "retry": "retry",
        "continue": "extract",
    },
)

# continue graph execution
graph.add_edge("retry", "extract")
graph.add_edge("extract", "synthesize")
graph.add_edge("synthesize", END)

# compile graph
app = graph.compile()

result = app.invoke(
    {
        "urls": [
            "https://www.cnet.com",
            "https://arstechnica.com",
            "https://techcrunch.com",
        ],
        "results": [],
        "extracted": [],
        "briefing": "",
        "current_url": "",
        "status": "",
        "retry_count": 0,
    }
)

print("\nExtracted fields:")
print(result["extracted"])

print("\nFinal briefing:")
print(result["briefing"])

print("\nStatus:", result["status"])