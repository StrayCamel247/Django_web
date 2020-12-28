#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ :
# __REFERENCES__ : 作者为moofeng
# __date__: 2020/12/28 15

import datetime
import pandas as pd
import requests
from lxml import etree


def handle_code_list(func):
    def wrapper(self, code_list):
        if isinstance(code_list, str):
            return func(self, code_list)
        else:
            return [func(self, code) for code in list(code_list)]
    return wrapper


class JQ:
    def __init__(self):
        import jqdatasdk
        self._sdk = jqdatasdk
        self._sdk.auth('15207124654', 'xiaoyv2Quant')
        self.today = datetime.datetime.today()

    @handle_code_list
    def normalize_code(self, code):
        return self._sdk.normalize_code(code)

    @handle_code_list
    def get_last_close(self, code):
        return self._sdk.get_price(code,
                                   count=1,
                                   end_date=self.today,
                                   frequency='daily',
                                   fields=None,
                                   skip_paused=True,
                                   fq='pre',
                                   panel=False).close.iloc[0]

    @handle_code_list
    def get_security_name(self, code):
        return self._sdk.get_security_info(code).display_name

    @handle_code_list
    def get_industry(self, code):
        return self._sdk.get_industry(
            code)[code]['sw_l2']['industry_name'].replace('II', '')

    @handle_code_list
    def get_valuation(self, code):
        q = self._sdk.query(
            self._sdk.valuation
        ).filter(
            self._sdk.valuation.code == code
        )
        return self._sdk.get_fundamentals(q)[['pe_ratio', 'pb_ratio', 'ps_ratio', 'pcf_ratio']].iloc[0]


class ParseQDII:
    def __init__(self):
        self.domain = 'https://palmmicro.com'

    def get_stock_data(self, code: '股票code' = 'sz162411'):
        '''获取华宝油气每日折溢价数据
        '''
        url = f"{self.domain}/woody/res/{code}cn.php"
        re = requests.get(url)
        re.encoding = 'utf-8'
        root = etree.HTML(re.text)
        data = {}
        data['code'] = code.upper()
        data['price'] = root.xpath(
            '//*[@id="reference"]/tr[2]/td[2]/font/text()')[0]
        data['net_value'] = root.xpath(
            '//*[@id="estimation"]/tr[2]/td[2]/text()')[0]
        data['official_estimation'] = root.xpath(
            '//*[@id="estimation"]/tr[2]/td[3]/font/text()')[0]
        data['official_premium'] = root.xpath(
            '//*[@id="estimation"]/tr[2]/td[4]/font/text()')[0]
        data['realtime_estimation'] = root.xpath(
            '//*[@id="estimation"]/tr[2]/td[7]/font/text()')[0]
        data['realtime_premium'] = root.xpath(
            '//*[@id="estimation"]/tr[2]/td[8]/font/text()')[0]
        return data


def get_conbond_data():
    '''数据来源： http://www.ninwin.cn/index.php?m=cb&a=cb_all
        序号    转债代码	转债名称	股票代码	股票名称	行业	子行业	转债价格	涨跌	日内套利	股价	涨跌.1	剩余本息	转股价格	转股溢价率	转股价值	距离转股日	剩余年限	回售年限	转债余额	转债成交额	转债换手率	余额/市值	余额/股本	股票市值	P/B	税前收益率	税后收益率	税前回售收益	税后回售收益	回售价值	纯债价值	弹性	信用	折现率	老式双低	老式排名	新式双低	新式排名	MA20乖离	热门度	转债名称.1	纯债溢价率
    '''
    url = "http://www.ninwin.cn/index.php?m=cb&a=cb_all"
    df = pd.read_html(url)[0]
    df['纯债溢价率'] = (df['转债价格'] / df['纯债价值'] -
                   1).apply(lambda x: round(x * 100, 2))
    df['转股溢价率'] = (df['转债价格'] / df['转股价值'] -
                   1).apply(lambda x: round(x * 100, 2))
    df['双低'] = df['纯债溢价率'] + df['转股溢价率']
    # df[['转债代码', '转债名称', '股票代码', '股票名称', '转债价格', '涨跌', '股价', '涨跌.1', '纯债价格', '转股价格', '纯债溢价率', '转股溢价率', '双低']]
    df = df.sort_values(by=['双低'])
    df.to_excel('可转债市场数据.xlsx', index=False)


def read_excel(sdk, df: '处理好的持仓数据' = pd.DataFrame(), input_file='股票持仓.xlsx'):
    if df.empty:
        df = pd.read_excel(input_file, dtype={'code': 'str'})

    # 格式化股票代码，如 000002 -> 000002.XSHE
    code_list = sdk.normalize_code(df.code)

    # 获取股票名称
    df['name'] = sdk.get_security_name(code_list)
    # 获取最近交易日收市价
    df['trade'] = sdk.get_last_close(code_list)
    # 计算股票市值
    df['value'] = df.num * df.trade
    # 计算股票盈亏
    df['profit'] = (df.trade - df.cost) * df.num
    # 计算股票涨跌幅
    df['rise'] = df.trade / df.cost - 1

    # 获取市盈率、市净率、市销率、市现率，表格数据保留两位小数
    valuation_df = pd.DataFrame(
        sdk.get_valuation(code_list)).reset_index(drop=True)
    df['pe_ratio'] = valuation_df.pe_ratio.round(decimals=2)
    df['pb_ratio'] = valuation_df.pb_ratio.round(decimals=2)
    df['ps_ratio'] = valuation_df.ps_ratio.round(decimals=2)
    df['pcf_ratio'] = valuation_df.pcf_ratio.round(decimals=2)

    # 计算单只股票仓位
    value_total = df['value'].sum()
    df['position'] = df['value'] / value_total

    # 获取股票所属行业
    df['industry'] = sdk.get_industry(code_list)
    return df


def make_excel(df, output_file='股票收益情况.xlsx'):
    df['position'] = df['position'].apply(lambda x: format(x, '.2%'))
    df['rise'] = df['rise'].apply(lambda x: format(x, '.2%'))
    # 重命名为中文列名
    df.rename(
        columns={
            'code': '编号',
            'name': '名称',
            'cost': '成本',
            'num': '股数',
            'trade': '现价',
            'value': '市值',
            'profit': '盈亏',
            'rise': '涨幅',
            'position': '仓位',
            'industry': '行业',
            'pe_ratio': '市盈率',
            'pb_ratio': '市净率',
            'ps_ratio': '市销率',
            'pcf_ratio': '市现率',
        }, inplace=True)
    # df.to_excel(output_file, index=False)


def make_charts(df):
    from pyecharts.charts import Bar
    from pyecharts import options as opts
    from pyecharts.globals import ThemeType
    df = df[['name', 'rise']].sort_values(by=['rise'], ascending=True)
    df['rise'] = round(df['rise'] * 100, 1)
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(df['name'].to_list())
        .add_yaxis('涨跌幅', df['rise'].to_list())
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(type_='value'),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts={"interval": 1}
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True, formatter='{c}%'))
    )
    bar.render('charts.html')


if __name__ == "__main__":
    get_conbond_data()
    sdk = JQ()
    df = read_excel(sdk)
    # make_charts(df)
    make_excel(df)
    s = ParseQDII()
    s.get_sz162411()
