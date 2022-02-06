import pandas as pd
from datetime import date
from abc import ABC, abstractmethod

from autoquant.provider import Provider
from autoquant.mixin.data import PriceMixin, StatementMixin
from autoquant import Market

from autoquant.provider.baostock import BaostockProvider
from autoquant.provider.snowball import SnowballProvider
from autoquant.log import logger


class _Collector(ABC):
    def __init__(self) -> None:
        self.price_providers = list()
        self.statement_providers = list()

    @classmethod
    def default(cls):
        return cls().with_price_provider(BaostockProvider()).with_statement_provider(SnowballProvider())

    def with_price_provider(self, provider: Provider):
        assert isinstance(provider, PriceMixin) and isinstance(provider, Provider), f'the parameter provider is not inherited from PriceMixin'
        self.price_providers.append(provider)
        return self

    def with_statement_provider(self, provider: Provider):
        assert isinstance(provider, StatementMixin) and isinstance(provider, Provider), f'the parameter provider is not inherited from StatementMixin'
        self.statement_providers.append(provider)
        return self


class Collector(PriceMixin, StatementMixin, _Collector):

    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):
        for provider in self.price_providers:
            try:
                return provider.daily_prices(market, code, start, end, **kwargs)
            except:
                logger.debug(f'failed to fetch daily prices from provider<{provider}>', exc_info=True)
        else:
            raise Exception('no valid data provider exsits for fetching daily prices')

    def quarter_statement(self, market: Market, code: str, quarter: date, **kwargs):
        for provider in self.statement_providers:
            try:
                return provider.quarter_statement(market, code, quarter, **kwargs)
            except:
                logger.debug(f'failed to fetch quarter statement from provider<{provider}>', exc_info=True)
        else:
            raise Exception('no valid data provider exsits for fetching quarter statement')
