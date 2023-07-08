# Quick Start

## Installation

```shell
pip install --upgrade autoquant
```


## Data Preparation 

```python
from autoquant.collector import Collector
from autoquant import Market
from datetime import date

collector = Collector.default()

data = collector.daily_prices(
    market=Market.SZ, 
    code='002594', 
    start=date(2021, 11, 1), 
    end=date(2021, 11, 5)
)

data = collector.quarter_statement(
    market=Market.SH, 
    code='601318', 
    quarter=date(2021, 9, 30)
)
    
```

## Backtest

```python


from autoquant.collector import Collector
from autoquant.workflow import Workflow
from autoquant.broker import Broker
from autoquant import Market
from datetime import date

from autoquant.workflow import Workflow
from autoquant.strategy import MA_CrossOver


class SmaCross(MA_CrossOver):
    params = dict(fast=5, slow=20)


collector = Collector.default()
broker = Broker.default(kick_start=100000, commission=0.01)

data = collector.daily_prices(market=Market.SZ, code='002594', start=date(2020, 1, 1), end=date(2021, 11, 1))
w = Workflow().with_broker(broker).with_strategy(SmaCross).backtest(data)

w.visualize()
```