from PySide6 import QtCore
from PySide6.QtCore import QObject

class Signaler(QObject):
    """
    Class for using QObject signals to communicate
    threads with main program.
    """
    # _ready = QtCore.Signal((str, str,))
    percent = QtCore.Signal()#(float,))
    ready = QtCore.Signal((str, float, float))

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

    # def signalReady(self, socket_id, text):
    #     self._ready.emit(socket_id, text)

    def signalReady(self, symbol, percent, tm):
        self.ready.emit(symbol, percent, tm)
        # print(f">>>>>>>>> SIGNAL")
         # signaler.percent.connect(self.socketReady)
        #@QtCore.Slot(str, str)
       # def socketReady(self, percent):

