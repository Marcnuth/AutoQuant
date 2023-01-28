from datetime import MAXYEAR, date
from abc import abstractmethod, ABCMeta

from autoquant import Market, StocksIndex, FundsIndex


class PriceMixin:
    @abstractmethod
    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):
        '''
        code: the stock code
        start: the start date
        end: then end date
        '''
        raise NotImplementedError


class StatementMixin:
    @abstractmethod
    def quarter_statement(self, market: Market, code: str, quarter: date, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def yearly_balance_sheet(self, market: Market, code: str,  years: list, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def yearly_income_sheets(self, market: Market, code: str, years: list, **kwargs):
        raise NotImplementedError


class IndexMixin:
    @abstractmethod
    def stocks_of_index(self, index: StocksIndex, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def funds_of_index(self, index: FundsIndex, **kwargs):
        raise NotImplementedError
