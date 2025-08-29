from typing import TypedDict


class GraphState(TypedDict):
    article_fetcher_result: str
    article_producer_agent_result: str
    humanize_agent_result: str
    translation_agent_result: str
    email_publication_result: str