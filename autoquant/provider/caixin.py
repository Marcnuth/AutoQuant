from pytest import mark
import requests
import arrow
import pandas as pd
from datetime import date, datetime

from . import Provider
from autoquant.mixin.data import StatementMixin
from autoquant import Market
from autoquant.log import logger

class CaixinProvider(StatementMixin, Provider):

    def __init__(self) -> None:
        pass

    @classmethod
    def __format_code(cls, market: Market, code: str):
        return {
            Market.SH: f'{code}.SH',
            Market.SZ: f'{code}.SZ',
            Market.HK: f'{code}',
            Market.US: f'{code}'
        }[market]

    @classmethod
    def __url_region(cls, market: Market):
        return {
            Market.SH: 'cn',
            Market.SZ: 'cn',
            Market.US: 'us',
            Market.HK: 'hk'
        }[market]

    @classmethod
    def __get(cls, market: Market, code: str, url: str, params: dict):
        formatted_code = cls.__format_code(market, code)

        ua = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'

        session = requests.session()
        data = session.get(f'https://s.ccxe.com.cn/api/stock/cgi/search?keyword={code}&page=1&size=20', headers={'User-Agent': ua})
        code_id = next((item['id'] for item in data.json()['data'] if item['code'] == formatted_code), None)
        assert code_id, f'cannot find code id based on {formatted_code}'

        params['code'] = code_id
        _url = f'{url}?{"&".join([f"{k}={str(v)}" for k,v in params.items()])}'
        data = session.get(_url, headers={
            'Host': 's.ccxe.com.cn',
            'Accept': 'application/json',
            'User-Agent': ua,
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })

        return data

    def quarter_statement(self, market: Market, code: str, quarter: date, **kwargs):
        pass

    def yearly_balance_sheet(self, market: Market, code: str, years: list, **kwargs):
        data = self.__get(market, code, f'https://s.ccxe.com.cn/api/stock/cgi/stockFinanceDebtReport', {
            'types': '4'
        })

        df = pd.DataFrame(data.json()['data'])
        df['market'], df['code'] = market, code
        df['year'] = df['endDate'].map(lambda x: arrow.get(x).year)
        df = df.query('year in @years')

        return pd.DataFrame({
            'market': market,
            'code': code,
            'year': df['year'],

            'asset_sum': df.get('assetSum'),                                                # 资产总计
            "debt_sum": df.get("debtSum"),                                                  # 负债合计
            "total_liabilities_and_ownerEquity": df.get("totalLiabilitiesAndOwnerEquity"),  # 负债和所有者权益（或股东权益）合计
            #-------------------------------流动资产---------------------------------
            'money_funds': df.get("moneyFunds"),                            # 货币资金
            'trading_financial_assets': df.get("tradingFinancialAssets"),   # 交易性金融资产
            'total_current_assets': df.get("totalCurrentAssets"),           # 流动资产合计
            #-------------------------------非流动资产---------------------------------
            "long_term_equity_investment": df.get("longTermEquityInvestment"),      # 长期股权投资
            "fixed_assets": df.get("fixedAssets"),                                  # 固定资产
            "construction_in_progress": df.get("constructionInProgress"),           # 在建工程
            "intangible_assets": df.get("intangibleAssets"),                        # 无形资产
            "goodwill": df.get("goodwill"),                                         # 商誉
            "deferredTaxAssets": df.get("deferredTaxAssets"),                       # 递延所得税资产
            "total_on_current_assets": df.get("totalNonCurrentAssets"),             # 非流动资产合计
            #-------------------------------流动负债---------------------------------
            "trading_financial_liabilities": df.get("tradingFinancialLiabilities"),  # 交易性金融负债
            "payroll_payable": df.get("payrollPayable"),                             # 应付职工薪酬
            "taxes_payable": df.get("taxesPayable"),                                 # 应交税费
            "total_current_liabilities": df.get("totalCurrentLiabilities"),          # 流动负债合计
            #-------------------------------非流动负债---------------------------------
            "estimated_liabilities": df.get("estimatedLiabilities"),                        # 预计负债
            "deferred_income_tax_liabilities": df.get("deferredIncomeTaxLiabilities"),      # 递延所得税负债
            "total_non_current_liabilities": df.get("totalNonCurrentLiabilities"),          # 非流动负债合计
            #-------------------------------所有者权益---------------------------------
            "paid_in_capital": df.get("paidInCapital"),                                     # 实收资本（或股本）
            "capital_reserve": df.get("capitalReserve"),                                    # 资本公积
            "surplus_reserve": df.get("surplusReserve"),                                    # 盈余公积
            "undistributed_profit": df.get("undistributedProfit"),                          # 未分配利润
            "parent_com_wwner_total_equity": df.get("parentComOwnerTotalEquity"),           # 归属于母公司所有者权益合计
            "minority_equity": df.get("minorityEquity"),                                    # 少数股东权益
            "total_owner_equity": df.get("totalOwnerEquity"),                               # 所有者权益（或股东权益）合计
        })

    def yearly_income_sheets(self, market: Market, code: str, years: list, **kwargs):
        pass

    def yearly_flow_sheets(self, market: Market, code: str, years: list, **kwargs):
        pass
