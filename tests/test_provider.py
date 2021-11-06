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
