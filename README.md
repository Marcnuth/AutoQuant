[![PypI Versions](https://img.shields.io/pypi/v/autoquant)](https://pypi.org/project/autoquant/#history)
![PyPI - Downloads](https://img.shields.io/pypi/dm/AutoQuant?label=PyPI)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyqlib.svg?logo=python&logoColor=white)](https://pypi.org/project/pyqlib/#files)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey)](https://pypi.org/project/autoquant/#files)


# AutoQuant

AutoQuant is an out-of-the-box quantitative investment platform.

It contains the full ML pipeline of data processing, strategy building(includes AI & traditionals), back-testing, and covers the entire chain of quantitative investment: alpha seeking, risk modeling, portfolio optimization, and order execution.

With AutoQuant, users can easily try ideas to create better Quant investment strategies.


- [AutoQuant](#autoquant)
- [Quick Start](#quick-start)
  - [Installation](#installation)
  - [Data Preparation](#data-preparation)
  - [Backtest](#backtest)
- [Advanced Topics](#advanced-topics)
  - [Market](#market)
  - [Metrics](#metrics)
    - [Exclusive Metrics](#exclusive-metrics)
    - [TA-Lib Metrics](#ta-lib-metrics)
  - [Price Provider](#price-provider)
  - [Financial Statement Provider](#financial-statement-provider)
- [Contribution Guide](#contribution-guide)
  - [Test](#test)
    - [Test all](#test-all)
    - [Test specified test](#test-specified-test)
  - [Development](#development)
    - [Generate Requirements](#generate-requirements)




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

# Advanced Topics

## Market
AutoQuant support Shanghai, Shenzhen, HongKong and US markets now.
Use Market Enum in codes:

```
from autoquant import Market

Market.SZ
Market.SH
Market.HK
Market.US
```

## Metrics

### Exclusive Metrics

- Gross Rate Of Return
- CAGR(Compound Annual Growth Rate) 


### TA-Lib Metrics
All the metrics in TA-Lib are available in AutoQuant.

For Example, if you were using the metrics of TA-Lib like this:
```
from talib import SMA

close = numpy.random.random(100)
output = MOM(close, timeperiod=5)
```

You can simply change the import sentence to use the metrics in AutoQuant. The codes would be:
```
from AutoQuant import SMA

close = numpy.random.random(100)
output = MOM(close, timeperiod=5)
```

## Price Provider

- BaostockProvider
- TushareProvider


## Financial Statement Provider

- SnowballProvider


# Contribution Guide

## Test
### Test all
```
PYTHONPATH=./ pytest
```

### Test specified test
```
PYTHONPATH=./ pytest tests/<YOUR_DISIRE_FILE>.py -k "<YOUR_DISIRE_TEST_CASE>" -s
```


## Development

### Generate Requirements

```
pipreqs ./ --encoding=utf8 --force
```