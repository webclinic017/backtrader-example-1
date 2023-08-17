from datetime import datetime
import backtrader as bt
import logging.config
import time

from data.dataset import CustomDataset
from strategies.abbration import Abbration
from strategies.bollkdj import BOLLKDJStrategy
from strategies.bollema import BollEMA
from strategies.boll import BollStrategy
from strategies.macdkdj import MACDKDJStrategy
from strategies.boll_reverser import BollReverser


class PrintClose(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        print(f'{dt} {txt}')  # Print date and close

    def next(self):
        self.log('Close: %.3f' % self.data0.close[0])


def float_range(start, stop, steps):
    return [start + float(i) * (stop-start) / (float(steps) - 1) for i in range(steps)]


if __name__ == '__main__':
    logging.config.fileConfig("logging.ini")
    logging.Formatter.converter = time.gmtime  #utc
    cerebro = bt.Cerebro(maxcpus=1)
    # cerebro.addstrategy(PrintClose)

    cerebro.addstrategy(BollStrategy, period_boll=220, slope=0.09)#, reversal=True)
    # cerebro.optstrategy(BollStrategy, period_boll=range(170, 270, 5), slope=0.99, debug=False)
    # cerebro.optstrategy(BollStrategy, period_boll=220, slope=float_range(0.05, 0.11, 7), debug=False)

    # cerebro.addstrategy(BollEMA)
    # cerebro.addstrategy(Abbration, boll_period=200)
    # cerebro.addstrategy(BOLLKDJStrategy, price_diff=30)
    # cerebro.addstrategy(MACDKDJStrategy)

    # cerebro.addstrategy(BollReverser)
    # cerebro.optstrategy(BollReverser, period_boll=range(100, 300, 20), debug=False)

    # cerebro.optstrategy(BOLLKDJStrategy, price_diff=range(5, 50,5), debug=False)

    # 加载数据
    data = CustomDataset(name="ETH",
                         dataname="data/ETHUSDT-1m-2023-07.csv",
                         dtformat=lambda x: datetime.utcfromtimestamp(int(x) / 1000),
                         timeframe=bt.TimeFrame.Minutes,
                         fromdate=datetime(2023, 1, 1),
                         todate=datetime(2023, 12, 31),
                         nullvalue=0.0)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=5)

    cerebro.broker.setcash(100.0)

    # 配置滑点费用,2跳
    # cerebro.broker.set_slippage_fixed(slippage*1)

    cerebro.broker.setcommission(commission=0.0004, margin=0.1, mult=1.0)
    # cerebro.broker.setcommission(commission=0.00075)

    cerebro.addsizer(bt.sizers.FixedSize, stake=1)
    # cerebro.addsizer(bt.sizers.PercentSizer, percents=100)

    # cerebro.addwriter(bt.WriterFile, out='log.csv', csv=True)

    cerebro.run()

    cerebro.plot()