from autoquant.collector import Collector
from autoquant.provider.snowball import SnowballProvider
from autoquant import Market
from datetime import date


def test_collect_daily_prices():
    collector = Collector.default()

    data = collector.daily_prices(market=Market.SZ, code='002594', start=date(2021, 11, 1), end=date(2021, 11, 5))
    assert data.shape[0] == 5
    assert data['code'][0] == 'sz.002594'

    data = collector.daily_prices(market=Market.SH, code='601318', start=date(2021, 11, 1), end=date(2021, 11, 5))
    assert data.shape[0] == 5
    assert data['code'][0] == 'sh.601318'


def test_collect_quarter_statement():
    collector = Collector.default()

    data = collector.quarter_statement(market=Market.SH, code='601318', quarter=date(2021, 9, 30))
    print(data)
