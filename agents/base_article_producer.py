from abc import ABC, abstractmethod

# Abstract base class for common functionality
class BaseArticleProducer():

    @abstractmethod
    def generate_article(self, article_fetcher_result):
        """
        Abstract method for article producer.
        """
        pass