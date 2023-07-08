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


def test_generate_hs300_finance_report():

    collector = Collector().with_index_provider(BaostockProvider()).with_statement_provider(CaixinProvider())

    data = collector.stocks_of_index(index=StocksIndex.HS300)
    data.to_csv('.output.hs300_index.csv', index=False)


    df = pd.DataFrame()
    for _, row in tqdm(data.iterrows(), total=data.shape[0]):
        m, code = row['market'], row['code']
        
        data = collector.yearly_balance_sheet(market=m, code=code, years=list(range(2017, 2022, 1)))
        df = pd.concat([df, data])

    df.to_csv('.output.hs300_yearly_financial_report.csv', index=False)