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
- [Advanced Topics](#advanced-topics)
  - [Market](#market)
  - [Metrics](#metrics)
  - [Price Provider](#price-provider)
  - [Financial Statement Provider](#financial-statement-provider)
- [Contribution Guide](#contribution-guide)
  - [Test](#test)
    - [Test all](#test-all)
    - [Test specified test](#test-specified-test)




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

- Gross Rate Of Return
- CAGR(Compound Annual Growth Rate) 

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

