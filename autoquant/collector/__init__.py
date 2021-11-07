import pandas as pd
from datetime import date
from abc import ABC, abstractmethod

from autoquant.provider import Provider
from autoquant.mixin.data import DataMixin
from autoquant import Market

from autoquant.provider.baostock import BaostockProvider
from autoquant.log import logger


class _Collector(ABC):
    def __init__(self) -> None:
        self.data_providers = list()

    @classmethod
    def default(cls):
        return cls().with_data_provider(BaostockProvider())

    def with_data_provider(self, provider: Provider):
        assert isinstance(provider, DataMixin) and isinstance(provider, Provider), f'the parameter provider is not inherited from DataMixin'
        self.data_providers.append(provider)
        return self


class Collector(DataMixin, _Collector):

    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):
        for provider in self.data_providers:
            try:
                return provider.daily_prices(market, code, start, end, **kwargs)
            except:
                logger.debug(f'failed to fetch daily prices from provider<{provider}>', exc_info=True)
        else:
            raise Exception('no valid data provider exsits for fetching daily prices')
