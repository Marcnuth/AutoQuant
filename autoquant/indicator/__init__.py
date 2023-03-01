import numpy as np
from backtrader.indicators import *
from scipy.stats import linregress


class ParityIndex(Indicator):
    _mindatas = 2

    lines = ('index', )
    params = (('ma_period', 20),)
    plotinfo = dict(plotabove=True)

    def next(self):
        _data0_sum = math.fsum(self.datas[0].get(size=self.p.ma_period))
        _data0_ma = _data0_sum / self.p.ma_period

        _data1_sum = math.fsum(self.data1.get(size=self.p.ma_period))
        _data1_ma = _data1_sum / self.p.ma_period

        self.lines.index[0] = 0 if _data1_ma <= 1e-4 else _data0_ma / _data1_ma


class AdjustedMomentum(Indicator):
    '''https://www.quant-investing.com/blog/how-to-find-stocks-on-the-move-with-a-better-momentum-indicator-exponential-regression
    '''
    lines = ('trend',)
    params = (('period', 90),)

    def __init__(self):
        self.addminperiod(self.params.period)

    def next(self):
        returns = np.log(self.data.get(size=self.p.period))
        x = np.arange(len(returns))
        slope, _, rvalue, _, _ = linregress(x, returns)
        annualized = (1 + slope) ** 252
        self.lines.trend[0] = annualized * (rvalue ** 2)
