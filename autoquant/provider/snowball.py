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

    def quarter_statement(self, market: Market, code: str, quarter: date, **kwargs):
        formatted_code = self.__format_code(market, code)

        ua = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'

        session = requests.session()
        session.get(f'https://xueqiu.com/S/{formatted_code}', headers={'User-Agent': ua})
        cookie = session.cookies.get_dict()
        token = cookie['xq_a_token']

        region = {
            Market.SH: 'cn',
            Market.SZ: 'cn',
            Market.US: 'us',
            Market.HK: 'hk'
        }[market]

        dt = int(datetime(quarter.year, ((quarter.month - 1) // 3 + 1) * 3, 30, 0, 0, 0, 1000).timestamp() * 1000)
        data = session.get(f'https://stock.xueqiu.com/v5/stock/finance/{region}/indicator.json?symbol={formatted_code}&type=all&is_detail=true&count=5&timestamp={dt}', headers={
            'Host': 'stock.xueqiu.com',
            'Accept': 'application/json',
            'Cookie': f'xq_a_token={token}',
            'User-Agent': ua,
            'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
            'Accept-Encoding': 'br, gzip, deflate',
            'Connection': 'keep-alive'
        })

        reports = data.json()['data']['list']
        for r in reports:
            dt = arrow.get(r['report_date'])
            if dt.year == quarter.year and dt.month == quarter.month:
                return pd.DataFrame({
                    'revenue': r['total_revenue'][0],
                    'net_profit': r['net_profit_atsopc'][0],
                    'eps': r['basic_eps'][0],
                    'avg_roe': r['avg_roe'][0]
                }, index=[arrow.get(r['report_date']).format('YYYYMM')])
        else:
            raise Exception(f'failed to find specified quarter statement in {list(map(lambda x: x["report_date"], reports))}')
