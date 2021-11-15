from autoquant.collector import Collector
from autoquant.strategy import Strategy
from autoquant.broker import Broker

import backtrader as bt


class Workflow:
    def __init__(self) -> None:
        self.collector = None
        self.strategy = None
        self.broker = None
        self._cerebro = bt.Cerebro()
        self._cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio', timeframe=bt.TimeFrame.Years)
        self._cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
        self._cerebro.addanalyzer(bt.analyzers.Returns, _name='Returns',  timeframe=bt.TimeFrame.Years)
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

    def backtest(self, data,  **kwargs):
        feeds = bt.feeds.PandasData(dataname=data, fromdate=data['datetime'][0], todate=data['datetime'][-1])
        self._cerebro.adddata(feeds)
        self._cerebro_results = self._cerebro.run()
        return self

    def visualize(self):
        self._cerebro.plot()
        return self

    def summary(self):
        return '\n'.join([
            f'[Overview]: Initial Capital={self.broker.kick_start:.2f}',
            f'[Overview]: Final Capital={self._cerebro.broker.getvalue():.2f}',
            f'[Metrics]: Sharp Ratio={self._cerebro_results[0].analyzers.SharpeRatio.get_analysis().get("sharperatio"):.4f}',
            f'[Metrics]: Max DrawDown={self._cerebro_results[0].analyzers.DrawDown.get_analysis().max["drawdown"]:.4f}%',
            f'[Metrics]: CAGR={self._cerebro_results[0].analyzers.Returns.get_analysis().get("rtot"):.4f}%',
        ])
