import uuid
from dataclasses import field, dataclass
from typing import Dict

import requests
from bs4 import BeautifulSoup
import re

from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")    # all the objects of the class Item belong to the collection "items"
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:  # the method should return a float
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        # pattern = re.compile(r"(\d+,?\d*\.\d\d)")  # d = digit, ? = optional, + = at least 1, * = at least 0
        # match = pattern.search(string_price)
        # found_price = match.group(1)
        # without_commas = found_price.replace(",", "")

        without_commas = string_price.replace("£", "").replace("Kč", "").replace(",", "").replace(" ", "")
        self.price = float(without_commas)
        return self.price

    def json(self) -> Dict:     # to be able to save the data into MongoDB
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }

