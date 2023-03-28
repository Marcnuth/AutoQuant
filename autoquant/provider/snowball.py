from pytest import mark
import requests
import arrow
import pandas as pd
from datetime import date, datetime

from . import Provider
from autoquant.mixin.data import StatementMixin
from autoquant import Market


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
        return pd.DataFrame({
            'revenue': report['total_revenue'][0],
            'net_profit': report['net_profit_atsopc'][0],
            'eps': report['basic_eps'][0],
            'avg_roe': report['avg_roe'][0]
        }, index=[arrow.get(report['report_date']).format('YYYYMM')])

    def yearly_balance_sheet(self, market: Market, code: str, years: list, **kwargs):
        def __yearly_balance_sheet(year):
            dt = int(datetime(year, 12, 31, 0, 0, 0, 1000).timestamp() * 1000)
            data = self.__get(market, code, f'https://stock.xueqiu.com/v5/stock/finance/{region}/balance.json', {
                'symbol': formatted_code, 'type': 'Q4', 'is_detail': 'true', 'count': '1', 'timestamp': dt
            })

            report = data.json()['data']['list'][0]
            return pd.DataFrame({
                #-------------- 资产核心数据
                'currency_funds': report['currency_funds'][0],  # 货币资金
                'account_receivable': report['account_receivable'][0],  # 应收账款
                'inventory': report['inventory'][0],  # 存货
                'tradable_fnncl_assets': report['tradable_fnncl_assets'][0],  # 交易性金融资产
                'fixed_asset_sum': report['fixed_asset_sum'][0],  # 固定资产
                'total_assets': report['total_assets'][0],  # 资产总计
                #-------------- 负债核心数据
                'st_loan': report['st_loan'][0],  # 短期借款
                'lt_loan': report['lt_loan'][0],  # 长期借款
                'total_liab': report['total_liab'][0],  # 负债合计
                # --------------所得者权益核心数据
                'shares': report['shares'][0],  # 实收资本（或股本）
                'undstrbtd_profit': report['undstrbtd_profit'][0],  # 未分配利润
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
            return pd.DataFrame({
                # -------------- 收入
                'revenue': report['revenue'][0],  # 营业收入
                # -------------- 费用
                'sales_fee': report['sales_fee'][0],  # 销售费用
                'manage_fee': report['manage_fee'][0],  # 管理费用
                'financing_expenses': report['financing_expenses'][0],  # 财务费用
                # -------------- 收益
                'invest_income': report['invest_income'][0],  # 投资收益
                # -------------- 损失
                'asset_impairment_loss': report['asset_impairment_loss'][0],  # 资产减值损失
                # -------------- 其他
                'net_profit': report['net_profit'][0],  # 净利润
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
            return pd.DataFrame({
                'ncf_from_oa': report['ncf_from_oa'][0],  # 经营活动产生的现金流量净额
                'ncf_from_ia': report['ncf_from_ia'][0],  # 投资活动产生的现金流量净额
                'ncf_from_fa': report['ncf_from_fa'][0],  # 筹资活动产生的现金流量净额
            }, index=[arrow.get(report['report_date']).format('YYYY')])

        formatted_code = self.__format_code(market, code)
        region = self.__url_region(market)
        dfs = [__yearly_flow_sheet(y) for y in years]
        return pd.concat(dfs)
