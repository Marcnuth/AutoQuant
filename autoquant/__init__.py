
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
