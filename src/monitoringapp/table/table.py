from flask_table import Table, Col


class ItemTable(Table):
    ID = Col('ID')
    SERVER_NAME = Col('SERVER_NAME')
    Ping = Col('Ping')


class Item(object):

    def __init__(self, ID, SERVER_NAME, Ping):
        self.ID = ID
        self.SERVER_NAME = SERVER_NAME
        self.Ping = Ping.average
        if SERVER_NAME is None:
            self.SERVER_NAME = "Error"
        if Ping is None:
            self.Ping = "Error"
        else:
            if Ping.average is None:
                self.Ping = "Error"


def url2Item(url):
    return Item(ID=url.id, SERVER_NAME=url.serverName, Ping=url.ping)


def urls2Items(urls):
    items = []
    for url in urls:
        items.append(url2Item(url))

    return items
