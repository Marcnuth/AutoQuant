import datetime
import re
import arrow
import pandas as pd
from datetime import date
import requests
from bs4 import BeautifulSoup

from . import Provider
from autoquant.mixin.data import IndexMixin, PriceMixin
from autoquant import Market, FundsIndex

from cachetools.func import ttl_cache


class EastmoneyProvider(PriceMixin, IndexMixin, Provider):
    _UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    _API_FUNDS_INDEX = "http://fund.eastmoney.com/js/fundcode_search.js"
    _API_FUNDS_DETAIL = "http://fundf10.eastmoney.com/jbgk_{}.html"
    _API_DAILY_PRICES = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={}&page={}&sdate={}&edate={}&per={}"

    @ttl_cache(maxsize=5000, ttl=60 * 60 * 24)
    def daily_prices(self, market: Market, code: str, start: date, end: date, **kwargs):
        def __html(fund_code, start_date, end_date, page=1, per=40):
            url = self._API_DAILY_PRICES.format(fund_code, page, start_date, end_date, per)
            HTML = requests.get(url, headers={'User-Agent': self._UA})
            HTML.encoding = "utf-8"
            page_cnt = re.findall(r'pages:(.*),', HTML.text)[0]
            return HTML, int(page_cnt)

        def __parse(HTML):
            soup = BeautifulSoup(HTML.text, 'html.parser')
            trs = soup.find_all("tr")
            res = []
            for tr in trs[1:]:
                date = tr.find_all("td")[0].text  # 净值日期
                unit_net = tr.find_all("td")[1].text  # 单位净值
                acc_net = tr.find_all("td")[2].text  # 累计净值
                fund_r = tr.find_all("td")[3].text  # 日增长率
                buy_status = tr.find_all("td")[4].text  # 申购状态
                sell_status = tr.find_all("td")[5].text  # 赎回状态
                res.append([date, unit_net, acc_net, fund_r, buy_status, sell_status])
            df = pd.DataFrame(res, columns=['净值日期', '单位净值', '累计净值', '日增长率', '申购状态', '赎回状态'])

            return df

        assert market == Market.CN, 'only Market.CN is supported in EastmoneyProvider::daily_prices'
        html, pages = __html(code, start, end)
        res_df = pd.DataFrame()
        for page in range(pages):
            html, _ = __html(code, start, end, page=page + 1)
            df_ = __parse(html)
            res_df = pd.concat([res_df, df_])

        if res_df.size:
            df = pd.DataFrame({
                'market': market,
                'code': code,
                'datetime': res_df['净值日期'].map(lambda x: x.strip('*')).astype('datetime64[ns]'),
                'close': res_df['单位净值'].astype(float, errors='ignore'),
                'close_acc': res_df['累计净值'].astype(float, errors='ignore'),
                'pct_change': res_df['日增长率'].map(lambda x: x.strip('%')).astype(float, errors='ignore'),
                'status_purchase': res_df['申购状态'].map(lambda x: 'OPEN' if '开放' in x else 'CLOSE'),
                'status_redeem': res_df['赎回状态'].map(lambda x: 'OPEN' if '开放' in x else 'CLOSE')
            })
        else:
            df = pd.DataFrame([], columns=['market', 'code', 'datetime', 'close', 'close_acc', 'pct_change', 'status_purchase', 'status_redeem'])

        df.index = df['datetime']
        return df

    @ttl_cache(maxsize=5000, ttl=60 * 60 * 24)
    def funds_of_index(self, index: FundsIndex, **kwargs):
        @ttl_cache(maxsize=5000, ttl=60 * 60 * 24)
        def __detail(code):
            response = requests.get(self._API_FUNDS_DETAIL.format(code))
            soup = BeautifulSoup(response.text, 'lxml')
            table = soup.find_all("table")[1].find_all("td")

            return [
                table[2].get_text().replace("（前端）", ""),  # 基金代码
                table[8].get_text(),  # 基金公司
                table[10].get_text(),  # 基金经理
                table[5].get_text().split("/")[0].replace('年', '-').replace('月', '-').replace('日', '').strip(),  # 创建时间
                table[5].get_text().split("/")[1].strip().replace("亿份", ""),  # 基金份额
                table[3].get_text(),  # 基金类型
                table[18].get_text(),  # 业绩基准
                table[19].get_text(),  # 跟踪标的
            ]

        res = requests.get(self._API_FUNDS_INDEX, headers={'User-Agent': self._UA})
        res.encoding = "utf-8"
        list_ = eval(re.findall(r'\[.*\]', res.text)[0])
        df = pd.DataFrame(list_)
        df.columns = ['code', 'logogram', 'name', 'type', 'name_spell']

        all = pd.DataFrame({
            'updated_at': arrow.now().format('YYYY-MM-DD'),
            'market': Market.CN,
            'code': df['code'],
            'name': df['name'],
        })
        filtered = {
            FundsIndex.CN_ALL: lambda: all,
            FundsIndex.CN_ETF: lambda: all[all['name'].str.contains('ETF')],
            FundsIndex.CN_QDII: lambda: all[all['name'].str.contains('QDII')]
        }[index]()

        if not kwargs.get('details', False):
            return filtered

        details = [__detail(row['code']) for _, row in filtered.iterrows()]
        details = pd.DataFrame(details, columns=['code', 'company', 'manager', 'created_at', 'share', 'type', 'benchmark', 'tracking'])
        return pd.merge(filtered, details, on="code")
