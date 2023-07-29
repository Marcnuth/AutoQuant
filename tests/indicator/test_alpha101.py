import numpy as np
from scipy.stats import linregress
from autoquant.indicator.alpha101 import *
from autoquant import Market, StocksIndex
from autoquant.collector import Collector
from datetime import date
from autoquant.strategy import MA_CrossOver, Strategy
from autoquant.broker import Broker
from autoquant.workflow import Workflow
from autoquant.provider.eastmoney import EastmoneyProvider
import random
from autoquant.provider.local import LocalProvider
from pathlib import Path



def test_alpha101():

    data_dir = Path(__file__).parent.parent.parent / 'data'
    print(data_dir)

    collector = Collector().with_price_provider(LocalProvider(file_rglob='*.csv', dir=data_dir))

    data0 = collector.daily_prices(market=Market.SH, code='600809', start=date(2010, 1, 1), end=date(2011, 1, 1))
    data1 = collector.daily_prices(market=Market.SH, code='600745', start=date(2010, 1, 1), end=date(2011, 1, 1))


    class Test(Strategy):

        def __init__(self):
            self.a1 = WQA1()
            self.a2 = WQA2()
            self.a3 = WQA3()
            
        def next(self):
            #print('Alpha1:', self.a1[0])
            pass

    broker = Broker.default(kick_start=100000, commission=0.01)

    w = Workflow().with_broker(broker).with_strategy(Test).backtest(data0)
    # print(w.summary())
    w.visualize(crc=False, buysell=True, iplot=False)

