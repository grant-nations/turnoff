from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class Bot(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_articles(self) -> Tuple[List[Dict[str, str]],
                                    List[Dict[str, str]]]:
        """
        Get today's articles from the news source

        :return: Tuple:
            list of dictionaries with title, subtitle, and text of each article
            list of dictionaries with failed pages and their exceptions
        """
        pass
