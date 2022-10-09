import tushare as ts
import pandas as pd
from datetime import date
import arrow

from . import Provider
from autoquant.mixin.data import PriceMixin
from autoquant import Market


class TushareProvider(PriceMixin, Provider):

    def __init__(self, token) -> None:
        self.token = token
        self.ts_api = ts.pro_api(self.token)

    @classmethod
    def __format_code(cls, market: Market, code: str):
        return {
            Market.SH: f'{code}.SH',
            Market.SZ: f'{code}.SZ',
            Market.HK: f'{code}.HK',
            Market.US: f'{code}'
        }[market]

    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):

        fetch_daily_prices = {
            Market.SH: self.ts_api.daily,
            Market.SZ: self.ts_api.daily,
            Market.HK: self.ts_api.hk_daily,
            Market.US: self.ts_api.us_daily,
        }[market]

        formatted_code = self.__format_code(market, code)
        data = fetch_daily_prices(
            ts_code=formatted_code,
            start_date=arrow.get(start).format('YYYYMMDD'),
            end_date=arrow.get(end).format('YYYYMMDD')
        )

        df = pd.DataFrame({
            'market':  data['ts_code'].map(lambda x: Market[x.split('.')[0].upper()]),
            'code': data['ts_code'].map(lambda x: x.split('.')[-1]),
            'datetime': data['trade_date'].astype('datetime64[ns]'),
            'open': data['open'],
            'close': data['close'],
            'high': data['high'],
            'low': data['low'],
            'volume': data['vol'],
            'turnover': data['amount']
        })
        df.index = df['datetime']
        return df
