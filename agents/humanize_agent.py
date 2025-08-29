import gc
import logging
import threading

from langchain_ollama import OllamaLLM

class HumanizeAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = OllamaLLM(
            model="qwen3:1.7b",
            temperature=0
        )

    def __del__(self):
        logging.info("Cleaning up resources for Classification Agent")

    def humanize_text(self, comparison_result):
        """
        Classifiy files depending on results.
        """

        # Write the content to a Markdown file


        humanized_text = humanize_prompt(comparison_result)
        logging.info("Calling Tools usage with llm agent")


        return humanized_text



def run(state):
    try:
        # Create the agent instance
        task_thread_id = threading.get_ident()
        logging.info(f"Starting classification task on file {state['file_name']}, Thread ID: {task_thread_id}")
        agent = HumanizeAgent()

        # Perform the comparison
        report = agent.humanize_text(
            state['comparison_result']
        )

        logging.info(f"Finished classification task on file {state['file_name']}, Thread ID: {task_thread_id}")
    finally:
        # Ensure agent is deleted and garbage collection is triggered
        del agent
        gc.collect()

    # Return the comparison result
    return {"humanize_agent_result": report}
