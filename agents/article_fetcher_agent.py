import json
import logging
import feedparser
from newspaper import Article

class SourceDataFetcher:
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
        Returns a flat list of all articles.
        """
        articles = []
        seen_urls = set()

        for rss_url in self.feeds:
            feed_articles = self.fetch_articles_from_feed(rss_url, max_articles=articles_per_feed)
            count = 0
            for art in feed_articles:
                url = art['url']
                if url and url not in seen_urls:
                    full_art = self.fetch_full_article_content(url)
                    if full_art:
                        articles.append(full_art)
                        seen_urls.add(url)
                        count += 1
                if count >= articles_per_feed:
                    break

        # Pad with empty articles if less than expected
        expected_total = len(self.feeds) * articles_per_feed
        while len(articles) < expected_total:
            articles.append({
                "title": None,
                "content": None,
                "url": None
            })

        return {"articles": articles}


def run(state):
    """
    Entrypoint for fetching articles.
    """
    logging.info("Starting Article data fetcher (RSS version)")
    context = {}
    agent = SourceDataFetcher(context)
    output = agent.fetch_top_articles_json(articles_per_feed=5)
    with open("original_article_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    logging.info(f"Ending Article data fetcher output : {output}")
    return {"article_fetcher_result": output}
