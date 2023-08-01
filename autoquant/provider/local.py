import tushare as ts
import pandas as pd
from datetime import date
import arrow
from pathlib import Path
from collections import defaultdict


from . import Provider
from autoquant.mixin.data import PriceMixin, IndexMixin
from autoquant import Market
from autoquant.log import logger

class LocalProvider(PriceMixin, IndexMixin, Provider):

    def __init__(self, dir: Path) -> None:

        self.__price_data = pd.DataFrame()
        self.__index_data = pd.DataFrame()

        def __add_price_data(f):
            df = pd.read_csv(f.as_posix(), converters= {"market": lambda x: Market[x.upper()]})
            df['code'] = df['code'].astype(str)
            df['datetime'] = df['datetime'].astype('datetime64[ns]')
            if df.isnull().any().any():
                logger.warn(f'File<{f.name}> contains Nan Value!')

            self.__price_data = pd.concat([self.__price_data, df])

        def __add_index_data(f):
            pass

        handler = {
            'price': __add_price_data,
            'index': __add_index_data,
        }
        
        valid_files = (f for f in dir.rglob('*.csv') if f.is_file())
        for f in valid_files:
            handler.get(f.name.split('.')[-2], lambda _: None)(f)

    @classmethod
    def __format_code(cls, market: Market, code: str):
        return {
            Market.SH: f'{code}.SH',
            Market.SZ: f'{code}.SZ',
            Market.HK: f'{code}.HK',
            Market.US: f'{code}'
        }[market]


    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):

        df = self.__price_data.query('code == @code & market == @market & datetime >= @start & datetime <= @end')
        
        df.index = df['datetime']
        return df

    def all_index(self, market: Market, **kwargs):
        pass