import numpy as np
from scipy.stats import linregress
from autoquant.indicator import ParityIndex, RelativeMomentumIndex, RelativeStrengthIndex, OperationN, Momentum, AdjustedMomentum
from autoquant import Market, StocksIndex
from autoquant.collector import Collector
from datetime import date
from autoquant.strategy import MA_CrossOver, Strategy
from autoquant.broker import Broker
from autoquant.workflow import Workflow
from autoquant.provider.eastmoney import EastmoneyProvider
import random


def test_ParityIndex():

    start_date = date(2021, 1, 1)
    end_date = date(2021, 11, 5)

    collector = Collector.default()

    data0 = collector.daily_prices(market=Market.SH, code='000300', start=start_date, end=end_date)
    data1 = collector.daily_prices(market=Market.SH, code='000905', start=start_date, end=end_date)

    class Test(Strategy):

        def __init__(self):
            pi = ParityIndex()

    broker = Broker.default(kick_start=100000, commission=0.01)

    w = Workflow().with_broker(broker).with_strategy(Test).backtest(data0, data1)
    # print(w.summary())
    w.visualize(crc=False, buysell=True, iplot=False)


def test_RelativeMomentumIndex_RelativeStrengthIndex():
    start_date = date(2021, 1, 1)
    end_date = date(2021, 11, 5)

    collector = Collector.default()

    data0 = collector.daily_prices(market=Market.SH, code='000300', start=start_date, end=end_date)
    data1 = collector.daily_prices(market=Market.SH, code='000905', start=start_date, end=end_date)

    class Test(Strategy):

        def __init__(self):
            rmi = RelativeMomentumIndex()
            rsi = RelativeStrengthIndex()

    broker = Broker.default(kick_start=100000, commission=0.01)

    w = Workflow().with_broker(broker).with_strategy(Test).backtest(data0, data1)
    # print(w.summary())
    w.visualize(crc=False, buysell=True, iplot=False)


def momentum_func(self, the_array):
    r = np.log(the_array)
    slope, _, rvalue, _, _ = linregress(np.arange(len(r)), r)
    annualized = (1 + slope) ** 252
    return annualized * (rvalue ** 2)


class CustomMomentum(OperationN):
    lines = ('trend',)
    params = dict(period=12)
    func = momentum_func


def test_Momentum():

    start_date = date(2021, 1, 1)
    end_date = date(2021, 11, 5)

    collector = Collector.default()

    data0 = collector.daily_prices(market=Market.SH, code='000300', start=start_date, end=end_date)
    data1 = collector.daily_prices(market=Market.SH, code='000905', start=start_date, end=end_date)

    class Test(Strategy):

        def __init__(self):
            cm = CustomMomentum()
            m = Momentum()
            am = AdjustedMomentum(period=12)

    broker = Broker.default(kick_start=100000, commission=0.01)

    w = Workflow().with_broker(broker).with_strategy(Test).backtest(data0)
    # print(w.summary())
    w.visualize(crc=False, buysell=True, iplot=False)
