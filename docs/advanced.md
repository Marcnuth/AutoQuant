


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
FundsIndex.CN_QDII
FundsIndex.HUAXIA_SECTOR_ETF
```

## Indicators

### Specific Indicators
- ParityIndex
- AdjustedMomentum

### Backtrader Indicators
All the indicators in Backtrader are available in AutoQuant.

For Example, if you were using the indicators of Backtrader like this:

```python
from backtrader.indicators import Momentum
```

You can simply change the import sentence to use the indicators in AutoQuant. The codes would be:

```python
from autoquant.indicators import Momentum
```


## Metrics

### Specific Metrics

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

def yearly_flow_sheets(self, market: Market, code: str, years: list, **kwargs)

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
