
from enum import Enum, auto


class Market(Enum):
    SH = auto()
    SZ = auto()
    HK = auto()
    US = auto()
    CN = auto()  # 代指中国所有境内市场，沪/深/北


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


class FundsIndex(Enum):
    '''基金'''

    # A股
    CN_ETF = auto()  # A股ETF指数基金
    CN_ALL = auto()  # A股所有基金
    CN_QDII = auto()

    HUAXIA_SECTOR_ETF = auto()  # 华夏证券下的行业ETF基金
