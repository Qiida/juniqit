from src.monitoringapp.monitoringapp import MonitoringApp

import threading

from flask import Flask


monitoringApp = MonitoringApp()

flaskApp = Flask(__name__)


if __name__ == '__main__':
    monitoringApp_thread = threading.Thread(target=monitoringApp.run())
    monitoringApp_thread.start()
