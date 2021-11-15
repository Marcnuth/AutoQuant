from datetime import date
import numpy as np
import pandas as pd
from scipy import stats


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
