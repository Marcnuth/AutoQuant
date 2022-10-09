from autoquant.collector import Collector
from autoquant import Market, StocksIndex
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
    assert data.shape[1] == 4
    assert data['eps'][0] - 4.63 <= 1e-10
    assert data['avg_roe'][0] - 10.5 <= 1e-10

    data = collector.yearly_balance_sheet(market=Market.SZ, code='000002', years=[2019])
    assert data.shape[1] == 8
    assert data['total_liabilities'][0] - 1.459350e+12 <= 1e6
    assert data['total_shareholders_equity'][0] - 2.705791e+11 <= 1e5


def test_collect_yearly_income_sheets():
    collector = Collector.default()

    data = collector.yearly_income_sheets(market=Market.SZ, code='000002', years=[2011, 2020, 2009])
    print(data)


def test_query_index():
    collector = Collector.default()

    data = collector.stocks_of_index(index=StocksIndex.ZZ500)
    assert data.shape == (500, 4)

    data = collector.stocks_of_index(index=StocksIndex.HS300)
    assert data.shape == (300, 4)
    print(data)

    data = collector.stocks_of_index(index=StocksIndex.SZ50)
    assert data.shape == (50, 4)
