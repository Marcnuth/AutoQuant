import backtrader.indicators as btind
from autoquant.strategy import MA_CrossOver, Strategy
from autoquant.collector import Collector
from autoquant.workflow import Workflow
from autoquant.broker import Broker
from autoquant import Market
from datetime import date

from autoquant.workflow import Workflow
from autoquant.strategy import MA_CrossOver


class SmaCross(MA_CrossOver):
    # list of parameters which are configurable for the strategy
    params = dict(
        fast=5,  # period for the fast moving average
        slow=20   # period for the slow moving average
    )


def test_strategy():

    collector = Collector.default()

    broker = Broker.default(kick_start=100000, commission=0.01)

    data = collector.daily_prices(market=Market.SZ, code='002594', start=date(2020, 1, 1), end=date(2021, 11, 1))
    w = Workflow().with_broker(broker).with_strategy(SmaCross).backtest(data)
    print(w.summary())
    w.visualize()


def test_ebo():

    P = 420785380281.06775
    from autoquant.collector import Collector

    class EBO(Strategy):

        def __init__(self):
            self._safe_price = P * 0.8 / 116.251e8
            self._expected_price = self._safe_price * 1.1

        def next(self):
            if self.data.close < self._safe_price:
                self.buy(size=1000)

            elif self.data.close >= 30:
                self.sell(size=1000)

    collector = Collector.default()

    broker = Broker.default(kick_start=100000, commission=0.01)

    data = collector.daily_prices(market=Market.SZ, code='000002', start=date(2020, 1, 1), end=date(2022, 1, 1))
    w = Workflow().with_broker(broker).with_strategy(EBO).backtest(data)
    print(w.summary())
    w.visualize(crc=False, buysell=True, iplot=False, width=20, height=10, dpi=600, tight=False)
