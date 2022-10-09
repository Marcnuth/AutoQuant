import pandas as pd
from datetime import date
from abc import ABC, abstractmethod

from autoquant.provider import Provider
from autoquant.mixin.data import PriceMixin, StatementMixin, IndexMixin
from autoquant import Market, StocksIndex

from autoquant.provider.baostock import BaostockProvider
from autoquant.provider.snowball import SnowballProvider
from autoquant.log import logger


class _Collector(ABC):
    def __init__(self) -> None:
        self.price_providers = list()
        self.statement_providers = list()
        self.index_providers = list()

    @classmethod
    def default(cls):
        return cls().with_price_provider(BaostockProvider()).with_index_provider(BaostockProvider()).with_statement_provider(SnowballProvider())

    def with_price_provider(self, provider: Provider):
        assert isinstance(provider, PriceMixin) and isinstance(provider, Provider), f'the parameter provider is not inherited from PriceMixin'
        self.price_providers.append(provider)
        return self

    def with_statement_provider(self, provider: Provider):
        assert isinstance(provider, StatementMixin) and isinstance(provider, Provider), f'the parameter provider is not inherited from StatementMixin'
        self.statement_providers.append(provider)
        return self

    def with_index_provider(self, provider: Provider):
        assert isinstance(provider, IndexMixin) and isinstance(provider, Provider), f'the parameter provider is not inherited from "IndexMixin"'
        self.index_providers.append(provider)
        return self


class Collector(PriceMixin, StatementMixin, IndexMixin, _Collector):

    @classmethod
    def __iter_providers(cls, providers: list, func_name: str, **kwargs):
        for provider in providers:
            try:
                return getattr(provider, func_name)(**kwargs)
            except:
                logger.debug(f'failed to fetch {func_name}from provider<{provider}>', exc_info=True)
        else:
            raise Exception(f'no valid provider exsits for fetching {func_name}, parameters: {kwargs}')

    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):
        return self.__iter_providers(self.price_providers, self.daily_prices.__name__, market=market, code=code, start=start, end=end, **kwargs)

    def quarter_statement(self, market: Market, code: str, quarter: date, **kwargs):
        return self.__iter_providers(self.statement_providers, self.quarter_statement.__name__, market=market, code=code, quarter=quarter, **kwargs)

    def yearly_balance_sheet(self, market: Market, code: str,  years: list, **kwargs):
        return self.__iter_providers(self.statement_providers, self.yearly_balance_sheet.__name__, market=market, code=code, years=years, **kwargs)

    def yearly_income_sheets(self, market: Market, code: str, years: list, **kwargs):
        return self.__iter_providers(self.statement_providers, self.yearly_income_sheets.__name__, market=market, code=code, years=years, **kwargs)

    def stocks_of_index(self, index: StocksIndex, **kwargs):
        return self.__iter_providers(self.index_providers, self.stocks_of_index.__name__, index=index, **kwargs)
