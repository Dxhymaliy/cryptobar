import sys

from PySide6.QtCharts import QSplineSeries
from PySide6.QtGui import QPen
# import Signaler

class DatePercentSeries(QSplineSeries):
    def __init__(self, color, date_time, percent=0, parent=None):
        super().__init__()
        # self._signaler = Signaler.Signaler()
        # self._percent = percent
        line_color = QPen(color)#Qt.green
        line_color.setWidth(2)
        self.setPen(line_color)
        # self.append(date_time.toMSecsSinceEpoch(), percent)-------

    # def signalPercent(self):
    #     self._signaler.signalPercent()