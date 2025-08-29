import logging
import os
import re
import threading

from langchain_ollama import OllamaLLM
from agents.base_article_producer import BaseArticleProducer


class ArticleProducerAgent2(BaseArticleProducer):
    def __init__(self):
        # Initialize the local Ollama LLM
        self.llm = OllamaLLM(
            model="gemma3:latest",
            temperature=0.7
        )
        # Directory for markdown articles
        self.articles_dir = "articles"
        os.makedirs(self.articles_dir, exist_ok=True)

    def generate_article(self, article_fetcher_result):
        self.clean_articles_folder(self.articles_dir)

        articles = article_fetcher_result.get("articles", [])
        rewritten_articles = []

        for idx, article in enumerate(articles):
            original_title = article.get("title") or "Untitled"
            original_content = article.get("content") or ""
            original_url = article.get("url") or ""

            if not original_title and not original_content:
                rewritten_articles.append({"title": None, "content": None})
                continue

            prompt = (
                "Rewrite the following news article so that both the title (as the first Markdown H1 heading, e.g., '# New Title') "
                "and the content are completely different from the original wording, "
                "but preserve all the information and meaning. Keep it about the same length as the original.\n\n"
                "You may add notes and definitions for technical terms in the article to enhance clarity.\n"
                "Return ONLY a valid Markdown file, starting with an H1 title, followed by the article content. "
                f"add the url of the original article at the end Url:{original_url}"
                "Do NOT include any JSON, explanations, comments, or code blocks. Only valid Markdown.\n\n"
                "Here is the original article:\n"
                f"Title: {original_title}\n"
                f"Content: {original_content}\n\n"
                "Please return your answer as a well-formatted Markdown article."
            )

            try:
                response = self.llm.invoke(prompt)
                clean_markdown = self._remove_think_blocks(response)
                markdown_title = self._extract_markdown_title(clean_markdown) or self._capitalize_title(original_title)
                filename = self._sanitize_filename(markdown_title)
                filepath = os.path.join(self.articles_dir, f"{filename}.md")

                # Write the markdown file
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(clean_markdown.strip())

                rewritten_articles.append({
                    "title": markdown_title,
                    "content": clean_markdown.strip()
                })

            except Exception as ex:
                logging.error(f"LLM invocation failed for article {idx}: {ex}")
                rewritten_articles.append({
                    "title": None,
                    "content": None
                })

        return {"articles": rewritten_articles}

    @staticmethod
    def _remove_think_blocks(text):
        # Remove any <think>...</think> blocks
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    @staticmethod
    def _extract_markdown_title(markdown_text):
        # Extract the first H1 heading as the title
        match = re.search(r'^\s*#\s+(.+)', markdown_text, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def _sanitize_filename(title):
        # Remove forbidden characters from filenames and limit length
        filename = re.sub(r'[\\/*?:"<>|]', "_", title)
        filename = filename.strip()
        return filename[:100] if filename else "untitled"

    @staticmethod
    def _capitalize_title(title):
        # Capitalize the first letter of each word (simple title case)
        return title.strip().title() if title else "Untitled"

    @staticmethod
    def clean_articles_folder(folder):
        """
        Delete all .md files in the specified articles folder.
        """
        if not os.path.exists(folder):
            logging.info(f"Folder '{folder}' does not exist. Nothing to clean.")
            return

        files_deleted = 0
        for filename in os.listdir(folder):
            if filename.endswith('.md'):
                file_path = os.path.join(folder, filename)
                try:
                    os.remove(file_path)
                    files_deleted += 1
                except Exception as ex:
                    logging.error(f"Failed to delete {file_path}: {ex}")
        logging.info(f"Cleaned {files_deleted} markdown files from '{folder}'.")

def run(state):
    """
    Entrypoint to run the ArticleProducerAgent2.
    Pass in state as a dict with key 'article_fetcher_result'.
    """
    agent = None
    try:
        task_thread_id = threading.get_ident()
        logging.info("Starting Article producer agent 2 task")
        agent = ArticleProducerAgent2()
        result = agent.generate_article(state['article_fetcher_result'])
        logging.info(f"Finished Article producer agent 2 task, Thread ID: {task_thread_id}")

        # Output rewritten article list to a JSON file (for traceability)
        import json
        with open("rewritten_article_output_2.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    finally:
        if agent:
            del agent

    return {"article_producer_agent_result": result}
