from autoquant.metric import gross_rate_of_return, CAGR, max_drawdown, beta
from datetime import date


def test_metrics():
    assert gross_rate_of_return(1, 11) == 10
    assert CAGR(1, 11, date(2021, 11, 1), date(2023, 5, 1)) - 4.96 < 0.01

    assert max_drawdown([1, 2, 3, 4, 5, 6, 7]) == 0
    assert max_drawdown([7, 6, 5, 4, 3, 2, 1]) - 0.85 < 0.01
    assert max_drawdown([10, 8]) - 0.2 < 0.01
    assert beta([1, 2, 3, 4], [3, 4, 5, 6]) - 5.1 < 0.01
