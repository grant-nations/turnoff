from abc import ABC, abstractmethod
from typing import List, Dict


class NewsBot(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_articles(self) -> List[Dict[str, str]]:
        """
        Get today's articles from the news source

        :return: list of dictionaries with source, title, subtitle, and text of each article
        """
        pass
