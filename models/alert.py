import uuid
from dataclasses import dataclass, field
from typing import Dict

from libs.mailgun import Mailgun
from models.item import Item
from models.model import Model
from models.user import User


@dataclass(eq=False)    # objects won't be comparable
class Alert(Model):
    collection: str = field(init=False, default="alerts")   # init=False: it cannot be modified when creating a new object
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item_id,
            "price_limit": self.price_limit,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()  # no need to call Item, item is defined in __init__
        return self.item.price

    def notify_if_price_reached(self) -> None:
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}")

            Mailgun.send_email(
                [self.user_email],
                f"Notification for {self.name}",
                f"Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address to check your item: {self.item.url}",
                f'<p>Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}.</p><p>Click <a href="{self.item.url}">here</a> to see your item.</p>')

