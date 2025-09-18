import chainlit as cl
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
from graph.graph import create_graph  # Your LangGraph pipeline builder


graph = create_graph()

@cl.on_chat_start
async def start():
    # Show ONE button to the user on start
    await cl.Message(
        content="Click the button below to fetch, generate, and publish an article.",
        actions=[
            cl.Action(name="generate_article",
                      label="Generate Article",
                      payload={}   # Required field
                      )
        ]
    ).send()

@cl.action_callback("generate_article")
async def handle_generate_article(action: cl.Action):
    # Remove the button after first click (no actions in following messages)
    await cl.Message(content="🚀 Running the article generator pipeline... Please wait.").send()
    try:
        # Run your LangGraph pipeline (adapt the input as needed)
        result = await cl.make_async(graph.invoke)({})

        # Show completion WITHOUT further action buttons
        await cl.Message(content=f"✅ Article generator pipeline completed!\n\nResult: {result}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Pipeline failed: {e}").send()

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)
