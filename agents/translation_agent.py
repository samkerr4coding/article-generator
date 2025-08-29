import gc
import logging
import os
import threading

from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_ollama import OllamaLLM


class TranslationAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = OllamaLLM(
            model="qwen3:1.7b",
            temperature=0
        )
        # Define the File SYstem tools
        self.working_directory = os.path.abspath('./')
        self.toolkit = FileManagementToolkit(root_dir=self.working_directory)
        self.tools = self.toolkit.get_tools()
        self.agent = initialize_agent(self.tools, self.llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                      verbose=True,
                                      agent_executor_kwards={"handle_parsing_errors": True})

    def __del__(self):
        logging.info("Cleaning up resources for Classification Agent")

    def classify_files(self, comparison_result):
        """
        Classifiy files depending on results.
        """

        return ""

def run(state):
    try:
        # Create the agent instance
        task_thread_id = threading.get_ident()
        logging.info(f"Starting classification task on file {state['file_name']}, Thread ID: {task_thread_id}")
        agent = TranslationAgent()

        # Perform the comparison
        report = agent.classify_files(
            state['comparison_result']
        )

        logging.info(f"Finished classification task on file {state['file_name']}, Thread ID: {task_thread_id}")
    finally:
        # Ensure agent is deleted and garbage collection is triggered
        del agent
        gc.collect()

    # Return the comparison result
    return {"translation_agent_result": report}
