from autoquant.provider.tushare import TushareProvider
from autoquant.collector import Collector
from autoquant.provider.baostock import BaostockProvider
from autoquant.provider.eastmoney import EastmoneyProvider
from autoquant.provider.snowball import SnowballProvider
from autoquant.provider.caixin import CaixinProvider
from autoquant import Market, FundsIndex, StocksIndex
from datetime import date
from tqdm import tqdm
import pandas as pd


def test_sm_corelations():
    '''
    理论上，半导体材料行业的各个厂家的增长情况应该与半导体行业内的大趋势一致。
    找出趋势不一致的公司
    '''
    pass