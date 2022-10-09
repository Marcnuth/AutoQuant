import imp
from autoquant.metric import gross_rate_of_return, CAGR, max_drawdown, beta, annualized_rate_of_return, avg_annualized_rate_of_return
from datetime import date
from autoquant import Market

import numpy as np
from autoquant.metric import SMA, MOM, ADX
from autoquant.collector import Collector


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


def test_talib():
    data = np.array([
        0.52705793, 0.51377956, 0.53478318, 0.51338812, 0.50748327, 0.50511363,
        0.50994516, 0.50208868, 0.50103558, 0.50835769, 0.51937371, 0.53498262,
        0.55796011, 0.55107343, 0.54197122, 0.55064494, 0.53449412, 0.5311102,
        0.54049307, 0.53701081, 0.54014613, 0.52740391, 0.53962466, 0.54135829,
        0.55959697, 0.57618591, 0.56737799, 0.54749328, 0.54011583, 0.52169773,
        0.50193716, 0.50103959, 0.49361386, 0.50882482, 0.49286017, 0.49787659,
        0.4947294,  0.49199394, 0.48213119, 0.46759727, 0.45068783, 0.42956238,
        0.40232669, 0.39840755, 0.39117906, 0.38273883, 0.3881257,  0.3947352,
        0.39846174, 0.37951541, 0.37319101, 0.35553805, 0.36176935, 0.35577653,
        0.35682804, 0.36262759, 0.38008991, 0.3948669,  0.40917824, 0.40035211,
        0.40740183, 0.41060818, 0.39946119, 0.39660686])

    output = MOM(data, timeperiod=5)
    assert output[-1] - (-1.257138e-02) < 1e-8

    output = SMA(data)
    assert output[-1] - 0.41024082 < 1e-8

    collector = Collector.default()
    data = collector.daily_prices(market=Market.SH, code='600036', start=date(2020, 1, 1), end=date(2021, 1, 1))

    output = ADX(data['high'], data['low'], data['close'], timeperiod=14)
    assert output[-1] - 19.176119 < 1e-8
    print(output)

    import pandas as pd
    import matplotlib.pyplot as plt
    plot_data = pd.DataFrame({
        'high': data['high'],
        'low': data['low'],
        'close': data['close'],
        'adx': output
    })

    import seaborn as sns
    sns.lineplot(data=plot_data, palette="tab10", linewidth=1)
    plt.show()
