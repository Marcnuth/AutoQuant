from autoquant.metric import gross_rate_of_return, CAGR, max_drawdown, beta, annualized_rate_of_return, avg_annualized_rate_of_return
from datetime import date
from autoquant import Market


def test_metrics():
    assert gross_rate_of_return(1, 11) == 10
    assert CAGR(1, 11, date(2021, 11, 1), date(2023, 5, 1)) - 4.96 < 0.01

    assert max_drawdown([1, 2, 3, 4, 5, 6, 7]) == 0
    assert max_drawdown([7, 6, 5, 4, 3, 2, 1]) - 0.85 < 0.01
    assert max_drawdown([10, 8]) - 0.2 < 0.01


def test_beta():
    beta(Market.SH, '000002', start=date(2020, 1, 1), end=date(2021, 1, 1))


def test_aror():
    data = annualized_rate_of_return(market=Market.SZ, code='000002', start_year=2010, end_year=2021)
    assert abs(data - 0.087) < 1e-3

    data = avg_annualized_rate_of_return(market=Market.SZ, code='000002', start_year=2010, end_year=2021)
    assert abs(data - 0.135) < 1e-3
