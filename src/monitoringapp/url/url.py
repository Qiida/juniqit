import re
import time
from itertools import count
from datetime import datetime
import numpy as np

from src.monitoringapp.url.check import ping


def matchPattern(pattern, strInput):
    match = re.search(pattern, strInput)
    return match


class Ping:
    def __init__(self, pings):
        try:
            self.pings = pings
            self.min = np.min(pings)
            self.max = np.max(pings)
            self.average = int(np.round(np.average(pings)))
        except ValueError:
            self.pings = pings
            self.pings = [None, None, None]
            self.min = None
            self.max = None
            self.average = None


class Url:
    iterator = count(start=0, step=1)

    def __init__(self, url):
        self.time = datetime.now()
        self.ping = Ping([])
        self.ip = None
        self.stdout = None

        self.id = next(Url.iterator)
        self.url = url
        self.serverName = self.__matchServerName()

        self.isBeingChecked = False

    def __matchServerName(self):
        match = re.search(re.compile('https?://([A-Za-z_\d.-]+).*'), self.url)
        if match:
            serverName = match.group(1)

            # a = re.search("www.", serverName)
            # if not a:
            #     serverName = None

            return serverName
        else:
            return self.url

    def __matchIP(self):
        match = re.search(re.compile(r"\[(\d+.{0,1}.+)]"), self.stdout)
        if match:
            return match.group(1)
        else:
            return None

    def __extractPing(self):
        matches = re.findall(re.compile(r"Zeit=([0-9]+)ms"), self.stdout)
        pings = []
        for match in matches:
            pings.append(int(match))

        return Ping(pings=pings)

    def __Ping(self):
        self.stdout = ping(self.serverName)

    def check(self):
        self.isBeingChecked = True
        self.stdout = ping(self.serverName)
        self.ip = self.__matchIP()
        self.ping = self.__extractPing()
        self.time = datetime.now()
        self.isBeingChecked = False


if __name__ == '__main__':
    urls = list()

    urls.append(Url("https://www.google.de"))
    urls.append(Url("https://sdfff.  outube.de"))

    urls[0].check()

    print(urls[0].ip)
    print(urls[0].serverName)
    print(urls[0].ping.average)


    t1=time.time()
    urls[1].check()
    t2=time.time()

    print(urls[1].ip)
    print(urls[1].serverName)
    print(urls[1].ping.average)
