
import random
import sys
sys.path.append('.')
sys.path.insert(0, '.')

from PySide6.QtCharts import QChartView
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow

from PySide6.QtCharts import QChart, QValueAxis, QDateTimeAxis
from PySide6.QtCore import Qt, Slot, QDateTime

import DatePercentSeries
import Signaler
# import Receiver
import ClientMDReceiver


class TickersViewPercent(QChart):
    colors=(Qt.green, Qt.darkYellow, Qt.cyan, Qt.red, Qt.blue, Qt.black, Qt.yellow, Qt.gray)
    def __init__(self, tickers, parent=None):
        super().__init__(QChart.ChartTypeCartesian, parent, Qt.WindowFlags())
        # self._timer = QTimer()

        self.__init_values()
        self.__init_axis_x()
        self.__init_axis_y()

        self._series = {id: DatePercentSeries.DatePercentSeries(color, self._curr)
                        for id, color in zip(tickers, TickersViewPercent.colors)}
        self._signaler = {id: Signaler.Signaler() for id in tickers}

        print(tickers)

        for id in self._series.keys():
            self.addSeries(self._series[id])
            self._signaler[id].ready.connect(self.handleReceive)
            print(f"~~~~~addSeries key={id}")


        self.addAxis(self._axisX, Qt.AlignBottom)
        self.addAxis(self._axisY, Qt.AlignLeft)

        for id in self._series.keys():
            self._series[id].attachAxis(self._axisX)
            self._series[id].attachAxis(self._axisY)
            print(f"~~~~~attachAxis key={id}")

        self._axisY.setRange(self._yMin, self._yMax)
        self._receiver = ClientMDReceiver.ClientMDReceiver(self._signaler)
        self._receiver.connectState.connect(lambda s: print("connect state : ",s))
        # self._receiver.startConnect("127.0.0.1",51300)
        self._receiver.startConnect("192.168.0.106",51300)
        self._receiver.waitForConnected()


    def __init_values(self):
        self._indx : int = 0
        self._step = 1

        self._cnt : int = 300 # increase to 300
        self._scroll_width = self._cnt / 10 #50
        self._yMax = 0.5
        self._yMin = -0.5


    def __init_axis_x(self):
        self._curr = QDateTime().currentDateTime() #.addSecs(1)
        self._axisX = QDateTimeAxis()
        self._axisX.setLabelsAngle(70)
        self._axisX.setFormat("mm:ss")
        self._axisX.setTitleText("Date")
        self._axisX.setTickCount(30)
        self._axisX.setRange(self._curr , self._curr.addSecs(self._cnt))
        self._sec : int = self._curr.toMSecsSinceEpoch()
        # print(f">>>>>  sec = {int(self._sec)}")


    def __init_axis_y(self):
        self._y = 0
        self._axisY = QValueAxis()
        self._axisY.setLabelFormat("%.3f") #????? to change float format
        self._axisY.setTitleText("Percent")
        self._axisY.setTickCount(11)

    @Slot()
    def handleReceive(self, symbol, percent, tm):
        if int(self._sec) != 0:
            self._indx = (tm - self._sec)/1000
            self._indx = self._indx % 10
            self._sec = 0
            print(f"~~~ index = {self._indx}")
        # else:
        self._indx = self._indx + 1
        # print(f"+++++ index = {self._indx}")

        self._series.get(symbol, None).append(tm, percent)
        # print(f"++++ tm:{tm} symbol:{symbol} percent:{percent}")

        # print(f"!!!!!!!!!!!!! 1 SLOT indx:{self._indx} _cnt:{self._cnt}")
        if self._indx > self._cnt:
            self.scroll(self.plotArea().width() / self._scroll_width, 0)
            print(f"~~~~~~~ 2 SLOT indx:{self._indx}  width: {self.plotArea().width()}")
            self._indx -= 10



if __name__ == "__main__":
    a = QApplication(sys.argv)
    window = QMainWindow()
    tickers = ["BTCUSDT"] #, "ETH"]
    chart = TickersViewPercent(tickers)
    chart.setTitle("Date Line chart")
    chart.legend().hide()
    chart.setAnimationOptions(QChart.AllAnimations)

    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)
    window.setCentralWidget(chart_view)
    window.resize(800, 400)
    window.show()

    sys.exit(a.exec())