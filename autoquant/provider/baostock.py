import baostock as bs
import arrow
import pandas as pd
from datetime import date, datetime

from . import Provider
from autoquant.mixin.data import PriceMixin
from autoquant import Market


class BaostockProvider(PriceMixin, Provider):

    def __init__(self) -> None:
        pass

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

        bs.login()
        try:
            data = bs.query_history_k_data_plus(
                formatted_code,
                "date,code,open,high,low,close,volume,amount",
                start_date=arrow.get(start).format('YYYY-MM-DD'),
                end_date=arrow.get(end).format('YYYY-MM-DD'),
                frequency="d"
            ).get_data()

            df = pd.DataFrame({
                'code': data['code'],
                'datetime': data['date'].astype('datetime64[ns]'),
                'open': data['open'].astype(float),
                'close': data['close'].astype(float),
                'high': data['high'].astype(float),
                'low': data['low'].astype(float),
                'volume': data['volume'].astype(float),
                'turnover': data['amount'].astype(float)
            })
            df.index = df['datetime']
            return df

        finally:
            bs.logout()
