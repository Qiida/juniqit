from src.monitoringapp.table.table import Item, ItemTable, urls2Items
from src.monitoringapp.url.url import Url


class TableBuilder:

    def __init__(self, items=None):

        if isinstance(items, list):
            self._ITEMS = items
        else:
            self._ITEMS = list()

        self._SERVER_NAMES = []
        self._IDS = []

    def put(self, item):

        self._ITEMS.append(item)
        self._SERVER_NAMES.append(item.serverName)
        self._IDS.append(item.ID)

    def putUrl(self, url):
        self._ITEMS.append(Item(url.id, url.serverName, url.ping))
        self._SERVER_NAMES.append(url.serverName)
        self._IDS.append(url.id)

    def construct(self, items=None):

        if items is None:
            return ItemTable(self._ITEMS)
        elif isinstance(items, list):
            return ItemTable(items)


if __name__ == '__main__':
    urls = list()

    urls.append(Url("https://www.google.de"))
    urls.append(Url("https://www.youtube.de"))
    urls.append(Url("https://www.stackoverflow.com"))
    urls.append(Url("https://www.geekforge.com"))

    TB = TableBuilder()
    for url in urls:
        TB.putUrl(url=url)

    itemTable = TB.construct()
    print(itemTable.__html__())

    TBwithList = TableBuilder(items=urls2Items(urls))
    table = TBwithList.construct()
    print(table.__html__())

