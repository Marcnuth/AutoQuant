from datetime import MAXYEAR, date
from abc import abstractmethod

from autoquant import Market


class PriceMixin:
    @abstractmethod
    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):
        '''
        code: the stock code
        start: the start date
        end: then end date
        '''
        pass


class StatementMixin:
    @abstractmethod
    def quarter_statement(self, market: Market, code: str, quarter: date, **kwargs):
        pass
