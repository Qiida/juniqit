import os
import time

from datetime import datetime

import threading
from flask import Flask

from src.monitoringapp.table.builder import TableBuilder
from src.monitoringapp.table.table import urls2Items
from src.monitoringapp.url.url import Url
from utils.system import ROOT_DIR

NUMBER_OF_THREADS = 16
MONITORING_FREQUENCY = 5


def initializeApp(MA=None):
    if MA is None:
        return Flask(__name__)
    else:
        if isinstance(MA, MonitoringApp):
            return MA
    return None


def initializeTableBuilder(TB=None):
    if TB is None:
        return TableBuilder()
    else:
        if isinstance(TB, TableBuilder):
            return TB
    return None


def startThreadToCheck(url):
    t = threading.Thread(url.check())
    t.start()
    return t


class MonitoringApp:

    def __init__(self, MA=None, TB=None):
        self.__path = os.path.join(ROOT_DIR, "urls.txt")
        self.__app = initializeApp(MA)
        self.tableBuilder = initializeTableBuilder(TB)
        self.urls = list()
        self.threads = dict()

        @self.__app.route('/')
        def home():
            return '<p>MonitoringApp!</p>'

        @self.__app.route('/table')
        def table():
            itemTable = self.tableBuilder.construct(items=urls2Items(self.urls))
            return itemTable.__html__()

    def getApp(self):
        return self.__app

    def getTableBuilder(self):
        return self.tableBuilder

    def putURL(self, url):
        urlObj = Url(url)
        self.urls.append(urlObj)

    def getUrls(self):
        return self.urls

    def load(self, p):
        if os.path.exists(p):
            path = p
        else:
            path = os.path.join(ROOT_DIR, p)

        self.__path = path

        try:
            f = open(path, mode='r')
            for line in f:
                self.urls.append(Url(line))
            print("URLs loaded up.")
        except FileNotFoundError:
            print("File not Found.")

    def add(self, url):
        f = open(self.__path, mode='w')
        f.write(url)
        self.urls.append(Url(url))

    def run(self):
        print("MonitoringApp")
        self.__printCommands()
        userInput = input("[IN]: ")

        while userInput != "exit" or userInput != "5":
            if userInput == "load" or userInput == "1":
                print("Path to URL List:")
                path = input()
                self.load(path)
                userInput = input("[IN]: ")

            elif userInput == "add" or userInput == "2":
                print("Add URL to List:")
                self.putURL(input())
                print("URL added.")
                userInput = input("[IN]: ")

            elif userInput == "run" or userInput == "3":
                print("Run FLASK App")
                self.threads.update({"t_monitoring": threading.Thread(target=self.startMonitoring())})
                self.threads.update({"t_flask": threading.Thread(target=self.__app.run())})



                print("Start Monitoring.")
                userInput = input("[IN]: ")

            elif userInput == "list" or userInput == "4":
                print("List of URLs:")
                for url in self.urls:
                    print(url.serverName)
                userInput = input("[IN]: ")

            elif userInput == "":
                print()
                userInput = input()

            elif userInput == "help":
                self.__printCommands()
                userInput = input("[IN]: ")

            elif userInput == "exit" or userInput == "5":
                return

            else:
                print("Error: unknown Command.")
                userInput = input("[IN]: ")

    def startThreads(self):
        for key in self.threads.keys():
            self.threads.get(key).start()


    def __printCommands(self):
        print("1: load")
        print("2: add")
        print("3: run")
        print("4: list")
        print("5: exit")
        print()
        print("type 'help' for commands")
        print()

    def __monitoring(self, url):
        current = datetime.now()
        difference = (current - url.time).total_seconds()
        if difference > MONITORING_FREQUENCY or not url.isBeingChecked:
            t = threading.Thread(target=url.check)
            t.start()
            return t

    def startMonitoring(self):

        numberOfThreads = 0

        while numberOfThreads < NUMBER_OF_THREADS:
            for url in self.urls:
                numberOfThreads += 1
                self.threads.update({"t_url_{}".format(url.id): self.__monitoring(url)})

    def endThreads(self):
        for key in self.threads.keys():
            self.threads.get(key).join()


if __name__ == '__main__':
    ma = MonitoringApp()
    ma.run()
