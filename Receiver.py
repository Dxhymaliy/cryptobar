# import random
# import string
# import threading

import os
import sys
sys.path.append('.')
sys.path.insert(0, '.')
import signal
# import uuid

from PySide6 import QtCore
from PySide6.QtNetwork import QTcpServer
from PySide6.QtNetwork import QHostAddress
from PySide6.QtCore import QObject, QCoreApplication

import json
# import DatePercentSeries
import Signaler
class Receiver(QObject):
    def __init__(self, signaler : dict[str: Signaler], parent=None):
        super(Receiver, self).__init__(parent)
        self._signaler = signaler
        self._server = QTcpServer(self)
        self.launch()
        self._server.newConnection.connect(self.on_newConnection)
        self._clients = {}

    def launch(self, address=QHostAddress.LocalHost, port=51300):
        return self._server.listen(QHostAddress(address), port)

    @QtCore.Slot()
    def on_newConnection(self):
        socket_descriptor = self._server.nextPendingConnection()
        socket_descriptor.readyRead.connect(self.on_readyRead)


    @QtCore.Slot()
    def on_readyRead(self):
        socket_descriptor = self.sender()
        resp = socket_descriptor.readAll()
        print(f"++++ receive: {resp}")

        indx = str(resp).find("}{")

        if indx > 0:
            self.parce_resp(resp[0:indx - 1:1]) #[indx + 1]
        else:
            self.parce_resp(resp)

    def parce_resp(self, resp):
        # print(f"++++ receive: {resp}")
        j = json.loads(resp.data())
        percent = j["p"] #percent
        symbol = j["s"] #.get("symbol")
        tm = j["E"] # .get("timestamp")
        i = str(j["i"])
        #
        if i == "1s":
            # print(f"++++ symbol: {symbol}")
            res = self._signaler.get(symbol, None)
            # print(f"++++ res: {res} - {tm}")
            if res != None:
                # res.append(tm, percent)
                res.signalReady(symbol, percent, tm)

def exit_handler(signal, frame):
    print('Exiting!')
    sys.exit(0)

def main():
    app = QCoreApplication(sys.argv)
    tickers = ["BTCUSDT", "ETHUSDT"]
    from PySide6.QtCore import Qt, QDateTime
    # colors=(Qt.green, Qt.darkYellow, Qt.cyan, Qt.red, Qt.blue, Qt.black, Qt.yellow, Qt.gray)
    signaler = {id: Signaler.Signaler() for id in tickers}
    server = Receiver(signaler)

    signal.signal(signal.SIGINT, exit_handler)
    return sys.exit(app.exec())

if __name__ == '__main__':
    main()