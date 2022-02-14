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
                'total_current_assets': report['total_current_assets'][0],
                'total_noncurrent_assets': report['total_noncurrent_assets'][0],
                'total_assets': report['total_assets'][0],
                'total_current_liabilities': report['total_current_liab'][0],
                'total_noncurrent_liabilities': report['total_noncurrent_liab'][0],
                'total_liabilities': report['total_liab'][0],
                'total_shareholders_equity': report['total_holders_equity'][0],
                'total_atsopc_equity': report['total_quity_atsopc'][0],
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
                'total_revenue': report['total_revenue'][0],
                'total_operating_costs': report['operating_costs'][0],
                'operating_profit': report['op'][0],
                'total_profit': report['profit_total_amt'][0],
                'net_profit': report['net_profit'][0],
                'net_profit_atsopc': report['net_profit_atsopc'][0],
                'other_comprehensive_income': report['othr_compre_income'][0],
                'total_comprehensive_income': report['total_compre_income'][0],
            }, index=[arrow.get(report['report_date']).format('YYYY')])

        formatted_code = self.__format_code(market, code)
        region = self.__url_region(market)
        dfs = [__yearly_income_sheet(y) for y in years]
        return pd.concat(dfs)
