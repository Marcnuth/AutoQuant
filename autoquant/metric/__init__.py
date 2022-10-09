# import all metrics from talib
from talib import *
from datetime import date
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from autoquant import Market, PriceAdjustment
from autoquant.collector import Collector


def gross_rate_of_return(initial_value, final_value):
    assert initial_value, f'initial value cannot be zero!'
    return (final_value - initial_value) / initial_value


def compound_annual_growth_rate(initial_value, final_value, start_date: date, end_date: date):
    assert end_date > start_date, f'end date must be larger than start date'
    r = gross_rate_of_return(initial_value, final_value)
    return np.power(1 + r, 365 / (end_date - start_date).days)


def CAGR(initial_value, final_value, start_date: date, end_date: date):
    return compound_annual_growth_rate(initial_value, final_value, start_date, end_date)


def sharp_ratio(r_p, r_f, sigma):
    return (r_p - r_f) / sigma


def max_drawdown(data):
    series = pd.Series(data)
    max_drawdown_i = series.rolling(series.size, min_periods=1).max()
    return (1 - series / max_drawdown_i).max()


def beta(target_vals: list, basic_vals: list):
    target = pd.Series(target_vals).pct_change()[1:]
    benchmark = pd.Series(basic_vals).pct_change()[1:]
    return stats.linregress(benchmark.values, target.values)[0]


def beta(market: Market, code: str, start: date, end: date):
    baseline_code = {
        Market.SH: '000001',
        Market.SZ: '399001',
        Market.HK: 'HSI',
        Market.US: 'SPY'
    }[market]

    collector = Collector.default()

    target_data = collector.daily_prices(market=market, code=code, start=start, end=end)
    baseline_data = collector.daily_prices(market=market, code=baseline_code, start=start, end=end)

    model = LinearRegression().fit(np.array(target_data['pct_change']).reshape((-1, 1)), baseline_data['pct_change'])
    return model.coef_[0]


def annualized_rate_of_return(market: Market, code: str, start_year: int, end_year: int):
    collector = Collector.default()
    data = collector.daily_prices(market=market, code=code, start=date(start_year, 1, 1), end=date(end_year, 12, 31), price_adjust=PriceAdjustment.SPLIT)
    simple_return = (data['close'][-1] - data['close'][0]) / data['close'][0]
    return pow(simple_return + 1, 1 / (end_year - start_year + 1)) - 1


def avg_annualized_rate_of_return(market: Market, code: str, start_year: int, end_year: int):
    aar = [annualized_rate_of_return(market, code, y, y) for y in range(start_year, end_year + 1)]
    return np.average(aar)
