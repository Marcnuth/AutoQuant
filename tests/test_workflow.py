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
