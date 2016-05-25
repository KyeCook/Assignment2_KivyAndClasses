from Assign1 import load_items
from item import Item


class ItemList:
    def __init__(self):
        self.items = []
        items = load_items()
        for item_list in items:
            # create Item object, put in self.items
            item = Item(item_list[0], item_list[1], float(item_list[2]), item_list[3])
            self.items.append(item)
