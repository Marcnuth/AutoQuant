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
  - [Data Provider](#data-provider)




# Quick Start

## Installation

```shell
pip install --upgrade autoquant
```


## Data Preparation 

```python
collector = Collector.default()
data = collector.daily_prices(market=Market.SZ, code='002594', start=date(2021, 11, 1), end=date(2021, 11, 5))
    
```

# Advanced Topics

## Data Provider

- BaostockProvider
- TushareProvider

