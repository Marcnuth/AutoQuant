
from enum import Enum, auto


class Market(Enum):
    SH = auto()
    SZ = auto()
    HK = auto()
    US = auto()


class PriceAdjustment(Enum):
    SPLIT = auto()  # 前复权
    REVERSE_SPLIT = auto()  # 后复权
    NONE = auto()


class StocksIndex(Enum):
    '''股票指数'''

    # A股
    ZZ500 = auto()  # 中证500
    HS300 = auto()  # 沪深300
    SZ50 = auto()  # 上证50
