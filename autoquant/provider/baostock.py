from collections import defaultdict
from multiprocessing import Value
from pickle import NONE
import baostock as bs
import arrow
import pandas as pd
from datetime import date, datetime

from . import Provider
from autoquant.mixin.data import IndexMixin, PriceMixin
from autoquant import Market, PriceAdjustment, StocksIndex


class BaostockProvider(PriceMixin, IndexMixin, Provider):

    def __init__(self) -> None:
        self.__adjustment_transformer = {
            PriceAdjustment.REVERSE_SPLIT: 1,
            PriceAdjustment.SPLIT: 2,
            PriceAdjustment.NONE: 3
        }

    @classmethod
    def __format_code(cls, market: Market, code: str):

        formatted = {
            Market.SH: f'sh.{code}',
            Market.SZ: f'sz.{code}'
        }.get(market, None)
        assert formatted is not None, f'market<{market.name}> is not supported yet, concat QQ:464848628 for more help'
        return formatted

    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):
        formatted_code = self.__format_code(market, code)
        adjust = self.__adjustment_transformer.get(kwargs.get('price_adjust', PriceAdjustment.NONE))

        bs.login()
        try:
            data = bs.query_history_k_data_plus(
                formatted_code,
                "date,code,open,high,low,close,volume,amount,pctChg",
                start_date=arrow.get(start).format('YYYY-MM-DD'),
                end_date=arrow.get(end).format('YYYY-MM-DD'),
                frequency="d",
                adjustflag=str(adjust),
            ).get_data()

            df = pd.DataFrame({
                'market':  data['code'].map(lambda x: Market[x.split('.')[0].upper()]),
                'code': data['code'].map(lambda x: x.split('.')[-1]),
                'datetime': data['date'].astype('datetime64[ns]'),
                'open': data['open'].astype(float),
                'close': data['close'].astype(float),
                'high': data['high'].astype(float),
                'low': data['low'].astype(float),
                'volume': data['volume'].astype(float),
                'turnover': data['amount'].astype(float),
                'pct_change': data['pctChg'].astype(float),
            })
            df.index = df['datetime']
            return df

        finally:
            bs.logout()

    def stocks_of_index(self, index: StocksIndex, **kwargs):
        func = {
            StocksIndex.ZZ500: bs.query_zz500_stocks,
            StocksIndex.HS300: bs.query_hs300_stocks,
            StocksIndex.SZ50: bs.query_sz50_stocks
        }[index]

        bs.login()
        try:
            data = func().get_data()
            return pd.DataFrame({
                'updated_at': data['updateDate'],
                'market':  data['code'].map(lambda x: Market[x.split('.')[0].upper()]),
                'code': data['code'].map(lambda x: x.split('.')[-1]),
                'name': data['code_name']
            })
        finally:
            bs.logout()
