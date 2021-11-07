from autoquant.provider.tushare import TushareProvider
from autoquant.collector import Collector
from autoquant.provider.baostock import BaostockProvider
from autoquant import Market
from datetime import date


def test_baostock():
    collector = Collector().with_data_provider(BaostockProvider())

    data = collector.daily_prices(market=Market.SZ, code='002594', start=date(2021, 11, 1), end=date(2021, 11, 5))
    assert data.shape[0] == 5
    assert data['code'][0] == 'sz.002594'

    data = collector.daily_prices(market=Market.SH, code='601318', start=date(2021, 11, 1), end=date(2021, 11, 5))
    assert data.shape[0] == 5


def test_tushare():

    collector = Collector().with_data_provider(TushareProvider(token='db07d243e5e7f246e4e53b94f79d88ad3c99aea7a700769dc0b1738b'))

    data = collector.daily_prices(market=Market.SZ, code='002594', start=date(2021, 11, 1), end=date(2021, 11, 5))
    assert data.shape[0] == 5
    assert data['code'][0] == '002594.SZ'
    assert data['open'][4] == 301.41
    assert data['close'][4] == 302.00
    assert data['high'][0] == 327.00
    assert data['low'][1] == 309.03
    assert data['volume'][2] == 197248.14
    assert data['turnover'][3] == 9102548.555

    data = collector.daily_prices(market=Market.SH, code='601318', start=date(2021, 11, 1), end=date(2021, 11, 5))
    assert data.shape[0] == 5
