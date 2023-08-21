from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class NewsBot(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_articles(self, verbose: bool) -> Tuple[List[Dict[str, str]],
                                                   List[Dict[str, str]]]:
        """
        Get today's articles from the news source

        :param verbose: if True, print progress to the console

        :return: Tuple:
            list of dictionaries with title, subtitle, and text of each article
            list of dictionaries with failed pages and their exceptions
        """
        pass
