import logging
import os
import re
import threading

import google.generativeai as genai
from agents.base_article_producer import BaseArticleProducer


class ArticleProducerAgent2(BaseArticleProducer):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

        genai.configure(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        self.model = genai.GenerativeModel(self.model_name)

        # Directories
        self.input_root = "articles/input"
        self.output_root = "articles/output"
        os.makedirs(self.output_root, exist_ok=True)
        os.makedirs(self.input_root, exist_ok=True)

        # Clean only output folder at start
        self.clean_articles_folder(self.output_root)

    @staticmethod
    def sanitize_title(title: str) -> str:
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
        return safe_title.strip()[:100] if title else "untitled"

    def load_articles_from_input(self):
        """
        Read all .md files from articles/input and return as a list of dicts.
        """
        articles = []
        for filename in os.listdir(self.input_root):
            if filename.endswith(".md"):
                filepath = os.path.join(self.input_root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    title = self._extract_markdown_title(content) or os.path.splitext(filename)[0]
                    articles.append({
                        "title": title,
                        "content": content,
                        "url": None  # not available in MD files
                    })
                except Exception as ex:
                    logging.error(f"Failed to read input file {filename}: {ex}")
        return articles

    def generate_article(self, _state=None):
        """
        Rewrite all articles from articles/input/*.md and save under articles/output/.
        """
        rewritten_articles = []
        from prompts.rewrite_prompt import get_rewrite_prompt

        input_articles = self.load_articles_from_input()
        logging.info(f"Found {len(input_articles)} articles in {self.input_root}")

        for idx, article in enumerate(input_articles, start=1):
            original_title = article.get("title") or "Untitled"
            original_content = article.get("content") or ""

            logging.info(f"[{idx}/{len(input_articles)}] Processing article: '{original_title}'")

            if not original_content.strip():
                logging.warning(f"[{idx}] Article '{original_title}' is empty, skipping.")
                rewritten_articles.append({"title": None, "content": None})
                continue

            try:
                prompt = get_rewrite_prompt(original_title, original_content, "")
                logging.debug(f"[{idx}] Prompt generated successfully for '{original_title}'")
            except Exception as ex:
                logging.error(f"[{idx}] Error generating prompt for '{original_title}': {ex}")
                rewritten_articles.append({"title": None, "content": None})
                continue

            try:
                response = self.model.generate_content(prompt).text
                logging.debug(f"[{idx}] Model response received for '{original_title}'")
            except Exception as ex:
                logging.error(f"[{idx}] LLM invocation failed for '{original_title}': {ex}")
                rewritten_articles.append({"title": None, "content": None})
                continue

            try:
                clean_markdown = self._remove_think_blocks(response)
                markdown_title = (
                        self._extract_markdown_title(clean_markdown)
                        or self._capitalize_title(original_title)
                )
                safe_title = self._sanitize_filename(markdown_title)

                # Create a folder for this article
                article_folder = os.path.join(self.output_root, safe_title)
                os.makedirs(article_folder, exist_ok=True)

                filepath = os.path.join(article_folder, f"{safe_title}.md")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(clean_markdown.strip())

                logging.info(f"[{idx}] Article '{markdown_title}' saved to {filepath}")

                rewritten_articles.append(
                    {"title": markdown_title, "content": clean_markdown.strip()}
                )
            except Exception as ex:
                logging.error(
                    f"[{idx}] Error during post-processing or saving for '{original_title}': {ex}"
                )
                rewritten_articles.append({"title": None, "content": None})

        logging.info(f"Finished processing {len(rewritten_articles)} articles.")
        return {"articles": rewritten_articles}

def run(state):
    """
    Entrypoint to run the ArticleProducerAgent2.
    """
    agent = None
    try:
        task_thread_id = threading.get_ident()
        logging.info("Starting Article producer agent 2 task")
        agent = ArticleProducerAgent2()
        result = agent.generate_article()
        logging.info(
            f"Finished Article producer agent 2 task, Thread ID: {task_thread_id}"
        )
    finally:
        if agent:
            del agent

    return {"article_producer_agent_result": result}
