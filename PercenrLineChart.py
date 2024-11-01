
import random
import sys
sys.path.append('.')
sys.path.insert(0, '.')

from PySide6.QtCharts import QChartView
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow

from PySide6.QtCharts import QChart, QValueAxis, QDateTimeAxis
from PySide6.QtCore import Qt, QTimer, Slot, QDateTime

import DatePercentSeries

class PercentLineChart(QChart):
    colors=(Qt.green, Qt.darkYellow, Qt.cyan, Qt.red, Qt.blue, Qt.black, Qt.yellow, Qt.gray)
    def __init__(self, tickers, parent=None):
        super().__init__(QChart.ChartTypeCartesian, parent, Qt.WindowFlags())
        self._timer = QTimer()

        self.__init_values()
        self.__init_axis_x()
        self.__init_axis_y()

        self._series = {id: DatePercentSeries.DatePercentSeries(color, self._curr) for id,
            color in zip(tickers, PercentLineChart.colors)}

        print(tickers)

        for id in self._series.keys():
            self.addSeries(self._series[id])
            print(f"~~~~~addSeries key={id}")

        self.addAxis(self._axisX, Qt.AlignBottom)
        self.addAxis(self._axisY, Qt.AlignLeft)

        for id in self._series.keys():
            self._series[id].attachAxis(self._axisX)
            self._series[id].attachAxis(self._axisY)
            print(f"~~~~~attachAxis key={id}")

        self._axisY.setRange(self._yMin, self._yMax)
                # !!! HERE !!! Need change to handle socket signal
        self._timer.timeout.connect(self.handleTimeout)
        self._timer.setInterval(1000)

        self._timer.start()

    def __init_values(self):
        self._indx = int(0)
        self._step = 1

        self._cnt = 60
        self._scroll_width = self._cnt / 10
        self._yMax = 50
        self._yMin = -50

    def __init_axis_x(self):
        self._curr = QDateTime().currentDateTime()
        self._axisX = QDateTimeAxis()
        self._axisX.setLabelsAngle(70)
        self._axisX.setFormat("mm:ss")
        self._axisX.setTitleText("Date")
        self._axisX.setTickCount(6)
        self._axisX.setRange(self._curr , self._curr.addSecs(self._cnt))

    def __init_axis_y(self):
        self._y = 0
        self._axisY = QValueAxis()
        self._axisY.setLabelFormat("%i")
        self._axisY.setTitleText("Percent")

    @Slot()
    def handleTimeout(self):
        now = QDateTime().currentDateTime().toMSecsSinceEpoch()
        for id in self._series.keys():
            self._series[id]._percent = random.uniform(self._yMin, self._yMax)
            print(f"~~~~~~~~`tm:{now}-percent:{self._series[id]._percent}")
            self._series[id].append(now, self._series[id]._percent)

        self._indx += 1
        if self._indx == self._cnt:
             self.scroll(self.plotArea().width() / self._scroll_width, 0)
             self._indx -= 10

        # if self._x == 100:
        #     self._timer.stop()

if __name__ == "__main__":
    a = QApplication(sys.argv)
    window = QMainWindow()
    tickers = ["BTC", "ETH"]
    chart = PercentLineChart(tickers)
    chart.setTitle("Date Line chart")
    chart.legend().hide()
    chart.setAnimationOptions(QChart.AllAnimations)

    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)
    window.setCentralWidget(chart_view)
    window.resize(800, 400)
    window.show()

    sys.exit(a.exec())