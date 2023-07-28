import tushare as ts
import pandas as pd
from datetime import date
import arrow
from pathlib import Path


from . import Provider
from autoquant.mixin.data import PriceMixin
from autoquant import Market
from autoquant.log import logger

class LocalProvider(PriceMixin, Provider):

    def __init__(self, file_rglob: str, dir: Path) -> None:

        self.__data = pd.DataFrame()

        for f in dir.rglob(file_rglob):
            if not f.is_file():
                continue

            assert f.suffix == '.csv', f'File<{f.name}> matches the rglob<{file_rglob}>, but the file format is not CSV. Only CSV file is supported!'
            df = pd.read_csv(f.as_posix(), converters= {"market": lambda x: Market[x.upper()]})
            df['code'] = df['code'].astype(str)
            df['datetime'] = df['datetime'].astype('datetime64[ns]')
            if df.isnull().any().any():
                logger.warn(f'File<{f.name}> contains Nan Value!')

            self.__data = pd.concat([self.__data, df])

    @classmethod
    def __format_code(cls, market: Market, code: str):
        return {
            Market.SH: f'{code}.SH',
            Market.SZ: f'{code}.SZ',
            Market.HK: f'{code}.HK',
            Market.US: f'{code}'
        }[market]


    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):

        df = self.__data.query('code == @code & market == @market & datetime >= @start & datetime <= @end')
        
        df.index = df['datetime']
        return df
