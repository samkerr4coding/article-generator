import json
import logging
import feedparser
import os
import re
from newspaper import Article
import concurrent.futures


class ArticleDataFetcher:
    # Curated list of high-quality AI/ML RSS feeds
    QUALITY_AI_RSS_FEEDS = [
        "https://arxiv.org/rss/cs.AI",
        "https://towardsdatascience.com/feed",
        "https://machinelearningmastery.com/blog/feed/",
        # "https://www.deepmind.com/blog/feed/basic",
        "https://www.kdnuggets.com/feed"
    ]

    def __init__(self, context=None):
        self.context = context or {}
        self.feeds = self.QUALITY_AI_RSS_FEEDS
        self.input_root = "articles/input"
        os.makedirs(self.input_root, exist_ok=True)

    def fetch_articles_from_feed(self, rss_url, max_articles=10):
        """
        Fetch up to max_articles article links from a given RSS feed.
        Returns a list of dicts: {'title', 'url'}
        """
        articles = []
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:max_articles]:
                url = entry.get('link') or entry.get('id')
                title = entry.get('title', 'No title')
                if url:
                    articles.append({'title': title, 'url': url})
        except Exception as ex:
            logging.warning(f"Could not parse RSS feed {rss_url}: {ex}")
        return articles

    def fetch_full_article_content(self, url):
        """
        Uses newspaper3k to extract article content from a URL.
        Returns a dict with title, content, and url if successful, else None.
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            if article.text and len(article.text) > 300:
                return {
                    "title": article.title or "No title",
                    "content": article.text,
                    "url": url
                }
        except Exception as ex:
            logging.debug(f"Failed to extract article from {url}: {ex}")
        return None

    def fetch_top_articles_json(self, articles_per_feed=10):
        """
        Fetches up to articles_per_feed articles' title/content/url from each RSS source.
        Saves each article as Markdown under articles/input.
        Returns a dict with all articles.
        """
        articles = []
        seen_urls = set()
        urls_to_fetch = []

        for rss_url in self.feeds:
            feed_articles = self.fetch_articles_from_feed(rss_url, max_articles=articles_per_feed)
            count = 0
            for art in feed_articles:
                url = art['url']
                if url and url not in seen_urls:
                    urls_to_fetch.append(url)
                    seen_urls.add(url)
                    count += 1
                if count >= articles_per_feed:
                    break

        # Parallel content extraction
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(self.safe_fetch, urls_to_fetch))
            articles = [art for art in results if art]

        # Save each article into articles/input as Markdown
        for article in articles:
            try:
                self.save_article_as_md(article)
            except Exception as ex:
                logging.error(f"Failed to save article '{article.get('title')}' to Markdown: {ex}")

        # Pad with empty articles if fewer than expected
        expected_total = len(self.feeds) * articles_per_feed
        while len(articles) < expected_total:
            articles.append({
                "title": None,
                "content": None,
                "url": None
            })

        return {"articles": articles}

    def safe_fetch(self, url):
        try:
            return self.fetch_full_article_content(url)
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction de l'article {url}: {e}")
            return None

    def sanitize_filename(self, title: str) -> str:
        filename = re.sub(r'[\\/*?:"<>|]', "_", title or "untitled")
        return filename.strip()[:100] if filename else "untitled"

    def save_article_as_md(self, article):
        """
        Save an article as Markdown in articles/input/<title>.md
        """
        title = article.get("title") or "Untitled"
        content = article.get("content") or ""
        url = article.get("url") or ""

        safe_title = self.sanitize_filename(title)
        filepath = os.path.join(self.input_root, f"{safe_title}.md")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"Source: {url}\n\n")
            f.write(content.strip())


def run(state):
    """
    Entrypoint for fetching articles.
    """
    agent = None
    try:
        logging.info("Starting Article data fetcher (RSS version)")
        context = {}
        agent = ArticleDataFetcher(context)
        output = agent.fetch_top_articles_json(articles_per_feed=10)

        with open("original_article_output.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        logging.info(f"Ending Article data fetcher output : {output}")

    finally:
        if agent:
            del agent
    return {"article_fetcher_result": output}
