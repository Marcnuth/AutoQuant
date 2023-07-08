from pytest import mark
import requests
import arrow
import pandas as pd
from datetime import date, datetime

from . import Provider
from autoquant.mixin.data import StatementMixin
from autoquant import Market
from autoquant.log import logger

class SnowballProvider(StatementMixin, Provider):

    def __init__(self) -> None:
        pass

    @classmethod
    def __format_code(cls, market: Market, code: str):
        return {
            Market.SH: f'SH{code}',
            Market.SZ: f'SZ{code}',
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
        session.get(f'https://xueqiu.com/S/{formatted_code}', headers={'User-Agent': ua})
        cookie = session.cookies.get_dict()
        token = cookie['xq_a_token']

        _url = f'{url}?{"&".join([f"{k}={str(v)}" for k,v in params.items()])}'
        data = session.get(_url, headers={
            'Host': 'stock.xueqiu.com',
            'Accept': 'application/json',
            'Cookie': f'xq_a_token={token}',
            'User-Agent': ua,
            'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
            'Accept-Encoding': 'br, gzip, deflate',
            'Connection': 'keep-alive'
        })

        return data

    def quarter_statement(self, market: Market, code: str, quarter: date, **kwargs):
        formatted_code = self.__format_code(market, code)
        region = self.__url_region(market)
        dt = int(datetime(quarter.year, ((quarter.month - 1) // 3 + 1) * 3, 30, 0, 0, 0, 1000).timestamp() * 1000)

        data = self.__get(market, code, f'https://stock.xueqiu.com/v5/stock/finance/{region}/indicator.json', {
            'symbol': formatted_code, 'type': 'all', 'is_detail': 'true', 'count': '1', 'timestamp': dt
        })

        report = data.json()['data']['list'][0]
        __safe_get = lambda key:  report.get(key, [None])[0]
        return pd.DataFrame({
            'revenue': __safe_get('total_revenue'),
            'net_profit': __safe_get('net_profit_atsopc'),
            'eps': __safe_get('basic_eps'),
            'avg_roe': __safe_get('avg_roe')
        }, index=[arrow.get(report['report_date']).format('YYYYMM')])

    def yearly_balance_sheet(self, market: Market, code: str, years: list, **kwargs):
        def __yearly_balance_sheet(year):
            dt = int(datetime(year, 12, 31, 0, 0, 0, 1000).timestamp() * 1000)
            data = self.__get(market, code, f'https://stock.xueqiu.com/v5/stock/finance/{region}/balance.json', {
                'symbol': formatted_code, 'type': 'Q4', 'is_detail': 'true', 'count': '1', 'timestamp': dt
            })

            report = data.json()['data']['list'][0]
            __safe_get = lambda key:  report.get(key, [None])[0]
            return pd.DataFrame({
                'market': market,
                'code': code,
                'year': year,
                #-------------- 资产核心数据
                'money_funds': __safe_get('currency_funds'),                                    # 货币资金
                'account_receivable': __safe_get('account_receivable'),                         # 应收账款
                'inventory': __safe_get('inventory'),                                           # 存货
                'trading_financial_assets': __safe_get('tradable_fnncl_assets'),                # 交易性金融资产
                'fixed_assets': __safe_get('fixed_asset'),                                      # 固定资产
                'asset_sum': __safe_get('total_assets'),                                        # 资产总计
                #-------------- 负债核心数据
                'st_loan': __safe_get('st_loan'),  # 短期借款
                'lt_loan': __safe_get('lt_loan'),  # 长期借款
                'total_liab': __safe_get('total_liab'),  # 负债合计
                # --------------所得者权益核心数据
                'shares': __safe_get('shares'),  # 实收资本（或股本）
                'undstrbtd_profit': __safe_get('undstrbtd_profit'),  # 未分配利润
            }, index=[arrow.get(report['report_date']).format('YYYY')])

        formatted_code = self.__format_code(market, code)
        region = self.__url_region(market)
        dfs = [__yearly_balance_sheet(y) for y in years]
        return pd.concat(dfs)

    def yearly_income_sheets(self, market: Market, code: str, years: list, **kwargs):
        def __yearly_income_sheet(year):
            dt = int(datetime(year, 12, 31, 0, 0, 0, 1000).timestamp() * 1000)
            data = self.__get(market, code, f'https://stock.xueqiu.com/v5/stock/finance/{region}/income.json', {
                'symbol': formatted_code, 'type': 'Q4', 'is_detail': 'true', 'count': '5', 'timestamp': dt
            })

            report = data.json()['data']['list'][0]
            __safe_get = lambda key:  report.get(key, [None])[0]
            return pd.DataFrame({
                # -------------- 收入
                'revenue': __safe_get('revenue'),  # 营业收入
                # -------------- 费用
                'sales_fee': __safe_get('sales_fee'),  # 销售费用
                'manage_fee': __safe_get('manage_fee'),  # 管理费用
                'financing_expenses': __safe_get('financing_expenses'),  # 财务费用
                # -------------- 收益
                'invest_income': __safe_get('invest_income'),  # 投资收益
                # -------------- 损失
                'asset_impairment_loss': __safe_get('asset_impairment_loss'),  # 资产减值损失
                # -------------- 其他
                'net_profit': __safe_get('net_profit'),  # 净利润
            }, index=[arrow.get(report['report_date']).format('YYYY')])

        formatted_code = self.__format_code(market, code)
        region = self.__url_region(market)
        dfs = [__yearly_income_sheet(y) for y in years]
        return pd.concat(dfs)

    def yearly_flow_sheets(self, market: Market, code: str, years: list, **kwargs):
        def __yearly_flow_sheet(year):
            dt = int(datetime(year, 12, 31, 0, 0, 0, 1000).timestamp() * 1000)
            data = self.__get(market, code, f'https://stock.xueqiu.com/v5/stock/finance/{region}/cash_flow.json', {
                'symbol': formatted_code, 'type': 'Q4', 'is_detail': 'true', 'count': '1', 'timestamp': dt
            })

            report = data.json()['data']['list'][0]
            __safe_get = lambda key:  report.get(key, [None])[0]
            return pd.DataFrame({
                'ncf_from_oa': __safe_get('ncf_from_oa'),  # 经营活动产生的现金流量净额
                'ncf_from_ia': __safe_get('ncf_from_ia'),  # 投资活动产生的现金流量净额
                'ncf_from_fa': __safe_get('ncf_from_fa'),  # 筹资活动产生的现金流量净额
            }, index=[arrow.get(report['report_date']).format('YYYY')])

        formatted_code = self.__format_code(market, code)
        region = self.__url_region(market)
        dfs = [__yearly_flow_sheet(y) for y in years]
        return pd.concat(dfs)
