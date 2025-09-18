import unittest
from agents.article_fetcher_agent import ArticleFetcherAgent

class TestArticleFetcherAgent(unittest.TestCase):
    def test_fetch_article(self):
        agent = ArticleFetcherAgent()
        # Remplacer par un test réel selon l'API de l'agent
        result = agent.fetch_article('dummy_url')
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()

