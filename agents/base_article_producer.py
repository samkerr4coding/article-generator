from abc import ABC, abstractmethod
import re
import os
import logging

# Abstract base class for common functionality
class BaseArticleProducer(ABC):
    @abstractmethod
    def generate_article(self, article_fetcher_result):
        """
        Abstract method for article producer.
        """
        pass

    @staticmethod
    def _remove_think_blocks(text):
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    @staticmethod
    def _extract_markdown_title(markdown_text):
        match = re.search(r'^\s*#\s+(.+)', markdown_text, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def _sanitize_filename(title):
        filename = re.sub(r'[\\/*?:"<>|]', "_", title)
        filename = filename.strip()
        return filename[:100] if filename else "untitled"

    @staticmethod
    def _capitalize_title(title):
        return title.strip().title() if title else "Untitled"

    @staticmethod
    def clean_articles_folder(folder):
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
