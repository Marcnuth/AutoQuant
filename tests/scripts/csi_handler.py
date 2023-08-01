'''
用于处理从 https://www.csindex.com.cn/#/ 导出的数据，以生成适用于 autoquant 格式的数据
'''
from pathlib import Path
import pandas as pd
import arrow
from autoquant import Market, Asset
import requests
from tqdm import tqdm
from time import sleep

def refactor_index_list(file):
    data = pd.read_excel(file)
    
    df = pd.DataFrame({
        'code': data['指数代码'],
        'name': data['指数简称'],
        'fullname': data['指数全称'],
        'close': data['最新收盘'],
        'currency': data['指数币种'].map(lambda x: {
            '人民币': 'RMB',
            '美元': 'USD',
            '港元': 'HKD',
            '欧元': 'EUR',
            '瑞士法郎': 'CHF',
        }[x]),
        'asset': data['资产类别'].fillna('').map(lambda x: {
            '股票': Asset.EQUILTY.name,
            '固定收益': Asset.BOND.name,
            '债券': Asset.BOND.name,
            '基金': Asset.FUND.name,
            '期货': Asset.FUTURE.name,
            '多资产': Asset.MULTI.name,
            '其他': Asset.OTHER.name,
        }[x]),
        'market': data['市场覆盖'].fillna('').map(lambda x: {
            '境内': Market.CN_MAINLAND.name,
            '沪深港': Market.CN.name,
            '香港': Market.HK.name,
            '全球': Market.GLOBAL.name,
            '': ''
        }[x]),
        'release_date': data['发布时间'],
        'basic_date': data['基日'],
        'release': data['基点'],
        'type': data['指数类别'],
        'n_constituent': data['样本数量'],
    })
    df['datetime'] = arrow.now().format('YYYY-MM-DD')
    df.to_csv(Path(__file__).parent.parent.parent / 'data'  / 'csi_export_all_2314_20230730.index.csv', index=False)

    return df

def refactor_index_products_list(file):
    pass

def download_constituents_of_index_file(codes):
    url = 'https://csi-web-dev.oss-cn-shanghai-finance-1-pub.aliyuncs.com/static/html/csindex/public/uploads/file/autofile/closeweight/{code}closeweight.xls'

    for c in tqdm(codes):
        target_file = Path(__file__).parent / f'{c}_constituents.xls'
        if target_file.exists():
            continue

        r = requests.get(
            url.format(code=c), 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        )
        if r.status_code != 200:
            print( f'[WARN]: fail to download file for code={c}, status code={r.status_code}')
            continue

        with open(target_file, 'wb+') as f:
            f.write(r.content)
        


def download_constituents_noweight_of_index_file(codes):
    url = 'https://csi-web-dev.oss-cn-shanghai-finance-1-pub.aliyuncs.com/static/html/csindex/public/uploads/file/autofile/cons/{code}cons.xls'
    for c in tqdm(codes):
        target_file = Path(__file__).parent / f'{c}_constituents_noweight.xls'
        if target_file.exists():
            continue

        r = requests.get(
            url.format(code=c), 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        )
        if r.status_code != 200:
            print( f'[WARN]: fail to download file for code={c}, status code={r.status_code}')
            continue

        with open(target_file, 'wb+') as f:
            f.write(r.content)


#----------------------------------------------------------------------------------
#
# Main
#
#----------------------------------------------------------------------------------

index_df = refactor_index_list(r'.\tests\scripts\指数列表.xlsx')

# 大部分指数都有包含权重的成分股文件，对于没有的指数，补充下载只有成分没有权重的文件。 注：存在指数两个文件都没有
# download_constituents_of_index_file(index_df['code'].tolist())
# noweight_codes = [c for c in index_df['code'] if not (Path(__file__).parent / f'{c}_constituents.xls').exists()]
# download_constituents_noweight_of_index_file(noweight_codes)
