from langgraph.constants import START, END
from langgraph.graph import StateGraph

from agents import article_producer_agent, comparison_agent, humanize_agent, \
    translation_agent, email_publication_agent, article_fetcher_agent
from state.graph_state import GraphState


def create_graph():
    global graph


    workflow = StateGraph(state_schema=GraphState)

    #Node initialization
    workflow.add_node("entry_point", lambda x: x)
    workflow.add_node("article_fetcher_agent", article_fetcher_agent.run)
   #  workflow.add_node("article_producer_agent1", article_producer_agent1.run)
    workflow.add_node("article_producer_agent", article_producer_agent.run)
    workflow.add_node("email_publication_agent", email_publication_agent.run)

    #graph definition
    workflow.add_edge(START, "entry_point")
    workflow.add_edge("entry_point", "article_fetcher_agent")
    # workflow.add_edge("source_article_fetcher", "article_producer_agent1")
    workflow.add_edge("article_fetcher_agent", "article_producer_agent")
    workflow.add_edge("article_producer_agent", "email_publication_agent")
    workflow.add_edge("email_publication_agent", END)


    # workflow.add_node("compare_results", comparison_agent.run)
    # workflow.add_node("humanize_result", humanize_agent.run)
    # workflow.add_node("translate_result", translation_agent.run)
    # workflow.add_node("publish_result", publication_agent.run)
    #
    # workflow.add_edge(["article_producer_agent1", "article_producer_agent"], "compare_results")
    # workflow.add_edge("compare_results", "humanize_result")
    # workflow.add_edge("humanize_result", "translate_result")
    # workflow.add_edge("classify_results", END)
    graph = workflow.compile()
    return graph
