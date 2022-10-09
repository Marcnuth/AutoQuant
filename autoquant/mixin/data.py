from datetime import MAXYEAR, date
from abc import abstractmethod

from autoquant import Market, StocksIndex


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

    @abstractmethod
    def yearly_balance_sheet(self, market: Market, code: str,  years: list, **kwargs):
        pass

    @abstractmethod
    def yearly_income_sheets(self, market: Market, code: str, years: list, **kwargs):
        pass


class IndexMixin:
    @abstractmethod
    def stocks_of_index(self, index: StocksIndex, **kwargs):
        pass
