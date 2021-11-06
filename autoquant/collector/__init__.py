import pandas as pd
from datetime import date
from abc import ABC, abstractmethod

from autoquant.provider import Provider
from autoquant.mixin.data import DataMixin
from autoquant import Market


class _Collector(ABC):
    def __init__(self) -> None:
        self.data_providers = list()

    def default(self):
        return self

    def with_data_provider(self, provider: Provider):
        self.data_providers.append(provider)
        return self


class Collector(DataMixin, _Collector):

    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):
        provider = next((p for p in self.data_providers), None)
        assert provider, 'no valid data provider exsits for fetching daily prices'
        return provider.daily_prices(market, code, start, end, **kwargs)
