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
  - [Index](#index)
  - [Metrics](#metrics)
    - [Exclusive Metrics](#exclusive-metrics)
    - [TA-Lib Metrics](#ta-lib-metrics)
  - [Providers](#providers)
    - [Price Provider](#price-provider)
      - [Provides List](#provides-list)
      - [API](#api)
    - [Financial Statement Provider](#financial-statement-provider)
      - [Provides List](#provides-list-1)
      - [API](#api-1)
    - [Index Provider](#index-provider)
      - [Provides List](#provides-list-2)
      - [API](#api-2)
- [Contribution Guide](#contribution-guide)
  - [Test](#test)
    - [Test all](#test-all)
    - [Test specified test](#test-specified-test)
  - [Development](#development)
    - [Generate Requirements](#generate-requirements)
    - [Package Update](#package-update)




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

```python
from autoquant import Market

Market.SZ
Market.SH
Market.HK
Market.CN
Market.US
```

## Index
AutoQuant support the indexes in multiple markets now.

Use StocksIndex Enum in codes:
```python
from autoquant import StocksIndex

StocksIndex.ZZ500
StocksIndex.HS300
StocksIndex.SZ50
```

Use FundsIndex Enum in codes:

```python
from autoquant import FundsIndex

FundsIndex.CN_ALL
FundsIndex.CN_ETF
```

## Metrics

### Exclusive Metrics

- Gross Rate Of Return
- CAGR(Compound Annual Growth Rate) 


### TA-Lib Metrics
All the metrics in TA-Lib are available in AutoQuant.

For Example, if you were using the metrics of TA-Lib like this:

```python
from talib import SMA

close = numpy.random.random(100)
output = MOM(close, timeperiod=5)
```

You can simply change the import sentence to use the metrics in AutoQuant. The codes would be:

```python
from AutoQuant import SMA

close = numpy.random.random(100)
output = MOM(close, timeperiod=5)
```


## Providers
### Price Provider

#### Provides List

- BaostockProvider
- TushareProvider
- EastmoneyProvider

#### API
```python
def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs)

```


### Financial Statement Provider


#### Provides List
- SnowballProvider


#### API

```python
def quarter_statement(self, market: Market, code: str, quarter: date, **kwargs)

def yearly_balance_sheet(self, market: Market, code: str,  years: list, **kwargs)

def yearly_income_sheets(self, market: Market, code: str, years: list, **kwargs)

```

### Index Provider


#### Provides List
- BaostockProvider
- EastmoneyProvider


#### API

```python
def stocks_of_index(self, index: StocksIndex, **kwargs)

def funds_of_index(self, index: FundsIndex, **kwargs)
```

# Contribution Guide

## Test
### Test all
```shell
PYTHONPATH=./ pytest
```

### Test specified test
```shell
PYTHONPATH=./ pytest tests/<YOUR_DISIRE_FILE>.py -k "<YOUR_DISIRE_TEST_CASE>" -s
```


## Development

### Generate Requirements

```shell
pipreqs ./ --encoding=utf8 --force
```
### Package Update

```shell
python3 -m build 
python3 -m twine upload dist/*
```