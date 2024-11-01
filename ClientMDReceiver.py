
import os
import sys
import signal
import json
# from PyQt6.uic.properties import QtCore

sys.path.append('.')
sys.path.insert(0, '.')

from PySide6 import QtCore

import Signaler


def exit_handler(signal, frame):
    print('Exiting!')
    sys.exit(0)

# def main():
#     app = QCoreApplication(sys.argv)
#     tickers = ["BTCUSDT", "ETHUSDT"]
#     from PySide6.QtCore import Qt, QDateTime
#     # colors=(Qt.green, Qt.darkYellow, Qt.cyan, Qt.red, Qt.blue, Qt.black, Qt.yellow, Qt.gray)
#     signaler = {id: Signaler.Signaler() for id in tickers}
#     server = Receiver(signaler)
#
#     signal.signal(signal.SIGINT, exit_handler)
#     return sys.exit(app.exec())
#
# if __name__ == '__main__':
#     main()


import socket
from PySide6.QtCore import *
from PySide6.QtNetwork import *


class ClientMDReceiver(QObject):

    # --------------- signals ---------------

    connectState = Signal(bool)
    # receiveData = Signal(QByteArray)

    def __init__(self, signaler : dict[str: Signaler], parent=None):
        super().__init__(parent)
        self._signaler = signaler
        # self._socket : QTcpSocket
        self._socket = QTcpSocket()
        self._socket.readyRead.connect(self.readData)
        # self._socket.readyWrite.connect(self._readData)
        self._socket.errorOccurred.connect(self.displayError)
        self._socket.connected.connect(lambda : self.connectState.emit(True))
        self._socket.disconnected.connect(lambda : self.connectState.emit(False))
        print("TcpClient()")

    def __del__(self):
        print("~TcpClient()")

    # --------------- func ---------------

    def startConnect(self, ip:str, port:int):
        self._socket.connectToHost(ip,port)
        pass

    def waitForConnected(self,msecs = 30000):
        self._socket.waitForConnected(msecs)
        pass

    def closeConnect(self):
        self._socket.disconnectFromHost()
        pass

    # def _writeData(self, data:QByteArray):
    #     self.connectState.emit(True)
    #     wret = self._socket.write(data)
    #     print(" writeData : {} , size : {}".format(data,wret))
    #     pass

    @QtCore.Slot()
    def displayError(self,err:QAbstractSocket.SocketError):
        print("{}".format(err))
        pass

    # @Slot()
    # def writeData(self):
    #     data = "ready"
    #     sz = self._socket.writeData("ready", len(data))
    #     if sz == len(data):
    #         print(f" _readData SEND >>>>>: size : {len(data)}")
    #     else:
    #         print(f" _readData SEND >>>>>: size:{len(data)} != send len:{sz}")
    #     pass

    @QtCore.Slot()
    def readData(self):
        print(" <<<<<<<< SLOT readData")
        # data = "ready"
        # if self._socket.writeData("ready", len(data)) == len(data):
        #     print(f" _readData SEND >>>>>: size : {len(data)}")
        bac = self._socket.bytesAvailable()
        resp = self._socket.readAll()
        print(" _readData : {} , size : {}".format(resp, bac))
        indx = str(resp).find("}{")

        if indx > 0:
            self.parce_resp(resp[0:indx - 1:1]) #[indx + 1]
        else:
            self.parce_resp(resp)
        pass

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


    def signalReceiveData(self):
        # self.receiveData.emit(ba)
        self._socket.readyRead.emit()
        print(" >>>>>>>>   send receiveData.emit")
        pass

if __name__ == "__main__":
    print(__name__,QThread.currentThread())
    app = QCoreApplication()
    try:
        tickers = ["BTCUSDT", "ETHUSDT"]
        # colors=(Qt.green, Qt.darkYellow, Qt.cyan, Qt.red, Qt.blue, Qt.black, Qt.yellow, Qt.gray)
        signaler = {id: Signaler.Signaler() for id in tickers}

        client = ClientMDReceiver(signaler)
        client.connectState.connect(lambda s: print("connect state : ",s))
        # client.startConnect("127.0.0.1",51300)
        client.startConnect("192.168.0.106",51300)
        client.waitForConnected()
    except  Exception as e :
        print(e)

    signal.signal(signal.SIGINT, exit_handler)
    sys.exit(app.exec())