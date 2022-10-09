import matplotlib.ticker as ticker  # 导入设置坐标轴的模块
import matplotlib.pyplot as plt
import pyfolio as pf
from autoquant.collector import Collector
from autoquant.strategy import Strategy
from autoquant.broker import Broker

import backtrader as bt
import pandas as pd


class Workflow:
    def __init__(self) -> None:
        self.collector = None
        self.strategy = None
        self.broker = None
        self._cerebro = bt.Cerebro()
        self._cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio', timeframe=bt.TimeFrame.Years)
        self._cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
        self._cerebro.addanalyzer(bt.analyzers.Returns, _name='Returns',  timeframe=bt.TimeFrame.Years)
        self._cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='TimeReturn')

        self._cerebro_results = None

    def with_collector(self, collector: Collector):
        assert isinstance(collector, Collector), f'the parameter collector should be Collector!'
        self.collector = collector
        return self

    def with_strategy(self, strategy: Strategy, **kwargs):
        # assert isinstance(strategy, Strategy), f'the strategy should be inherited from Strategy!'
        self.strategy = strategy
        self._cerebro.addstrategy(strategy)
        return self

    def with_broker(self, broker: Broker):
        self.broker = broker
        self._cerebro.broker.setcash(self.broker.kick_start)
        self._cerebro.broker.setcommission(self.broker.commission)
        return self

    def train(self, **kwargs):
        self.strategy.train()
        return self

    def backtest(self, *data,  **kwargs):
        for d in data:
            feeds = bt.feeds.PandasData(dataname=d, name=f'{d["market"][0].name}.{d["code"][0]}', fromdate=d['datetime'][0], todate=d['datetime'][-1])
            self._cerebro.adddata(feeds)
        self._cerebro_results = self._cerebro.run()
        return self

    def visualize(self, crc=True, buysell=False, **kwargs):
        def _plot_cum_return_curve():

            # 提取收益序列
            pnl = pd.Series(self._cerebro_results[0].analyzers.TimeReturn.get_analysis())
            # 计算累计收益
            cumulative = (pnl + 1).cumprod()
            # 计算回撤序列
            max_return = cumulative.cummax()
            drawdown = (cumulative - max_return) / max_return
            # 计算收益评价指标
            # 按年统计收益指标
            perf_stats_year = (pnl).groupby(pnl.index.to_period('y')).apply(lambda data: pf.timeseries.perf_stats(data)).unstack()
            # 统计所有时间段的收益指标
            perf_stats_all = pf.timeseries.perf_stats((pnl)).to_frame(name='all')
            perf_stats = pd.concat([perf_stats_year, perf_stats_all.T], axis=0)
            perf_stats_ = round(perf_stats, 4).reset_index()

            # 绘制图形
            plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
            plt.style.use('seaborn')  # plt.style.use('dark_background')

            fig, (ax0, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1.5, 4]}, figsize=(20, 8))
            cols_names = ['date', 'Annual\nreturn', 'Cumulative\nreturns', 'Annual\nvolatility',
                          'Sharpe\nratio', 'Calmar\nratio', 'Stability', 'Max\ndrawdown',
                          'Omega\nratio', 'Sortino\nratio', 'Skew', 'Kurtosis', 'Tail\nratio',
                          'Daily value\nat risk']

            # 绘制表格
            ax0.set_axis_off()  # 除去坐标轴
            table = ax0.table(cellText=perf_stats_.values,
                              bbox=(0, 0, 1, 1),  # 设置表格位置， (x0, y0, width, height)
                              rowLoc='right',  # 行标题居中
                              cellLoc='right',
                              colLabels=cols_names,  # 设置列标题
                              colLoc='right',  # 列标题居中
                              edges='open'  # 不显示表格边框
                              )
            table.set_fontsize(13)

            # 绘制累计收益曲线
            ax2 = ax1.twinx()
            ax1.yaxis.set_ticks_position('right')  # 将回撤曲线的 y 轴移至右侧
            ax2.yaxis.set_ticks_position('left')  # 将累计收益曲线的 y 轴移至左侧
            # 绘制回撤曲线
            drawdown.plot.area(ax=ax1, label='drawdown (right)', rot=0, alpha=0.3, fontsize=13, grid=False)
            # 绘制累计收益曲线
            (cumulative).plot(ax=ax2, color='#F1C40F', lw=3.0, label='cumret (left)', rot=0, fontsize=13, grid=False)
            # 不然 x 轴留有空白
            ax2.set_xbound(lower=cumulative.index.min(), upper=cumulative.index.max())
            # 主轴定位器：每 5 个月显示一个日期：根据具体天数来做排版
            ax2.xaxis.set_major_locator(ticker.MultipleLocator(300))
            # 同时绘制双轴的图例
            h1, l1 = ax1.get_legend_handles_labels()
            h2, l2 = ax2.get_legend_handles_labels()
            plt.legend(h1+h2, l1+l2, fontsize=12, loc='upper left', ncol=1)

            fig.tight_layout()  # 规整排版
            plt.show()

        if crc:
            _plot_cum_return_curve()

        if buysell:
            self._cerebro.plot(**kwargs)
        return self

    def summary(self):
        return '\n'.join([
            f'[Overview]: Initial Capital={self.broker.kick_start:.2f}',
            f'[Overview]: Final Capital={self._cerebro.broker.getvalue():.2f}',
            f'[Metrics]: Sharp Ratio={self._cerebro_results[0].analyzers.SharpeRatio.get_analysis().get("sharperatio"):.4f}',
            f'[Metrics]: Max DrawDown={self._cerebro_results[0].analyzers.DrawDown.get_analysis().max["drawdown"]:.4f}%',
            f'[Metrics]: CAGR={self._cerebro_results[0].analyzers.Returns.get_analysis().get("rtot"):.4f}%',
        ])
