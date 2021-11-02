import tushare as ts
import pandas as pd

from . import Provider
from autoquant.collector import CollectorMixin

class TushareProvider(CollectorMixin, Provider):

    def __init__(self, token) -> None:
        self.token = token
        self.ts_api = ts.pro_api(self.token)

    def daily_prices(code: str, date_range: pd.DatetimeIndex, **kwargs):
        pass


    