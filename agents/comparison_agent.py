import gc
import logging
import threading

from langchain_core.messages import HumanMessage
from langchain_ollama import OllamaLLM

from prompts.comparison_prompt import comparison_prompt


class ComparisonAgent:
    def __init__(self):
        # Initialize LLM (local or Azure-based)
        self.llm =  OllamaLLM(
                        model="qwen3:1.7b",
                        temperature=0
                    )

    def compare_results(self, file_name, article_producer_agent1_result, article_producer_agent_result):
        """
        Compare OCR results textually and via cosine similarity.
        """

        # Prepare a prompt with cosine similarities for LLM
        prompt = comparison_prompt(article_producer_agent1_result, article_producer_agent1_result, similarity_12)

        # Send the prompt to the LLM for detailed comparison
        response = self.llm([HumanMessage(content=prompt)])

        return {
            "content": response.content,
            "similarity": similarity_12,
            "file_name": file_name
        }

def run(state):
    try:
        # Create the agent instance
        task_thread_id = threading.get_ident()
        logging.info(f"Starting comparison task on both article generator results")
        agent = ComparisonAgent()

        # Perform the comparison
        comparison = agent.compare_results(
            state['article_producer_agent1_result'],
            state['article_producer_agent_result']
        )

        logging.info(f"Finished comparison task on on both article generator results")
    finally:
        # Ensure agent is deleted and garbage collection is triggered
        del agent
        gc.collect()

    # Return the comparison result
    return {"comparison_result": comparison}
