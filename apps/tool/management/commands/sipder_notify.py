from django.contrib.sitemaps import ping_google
import requests
from django.conf import settings


class SpiderNotify():
    # 提交百度统计
    @staticmethod
    def baidu_notify(urls):
        try:
            data = '\n'.join(urls)
            result = requests.post(settings.BAIDU_NOTIFY_URL, data=data)
            print(result.text)
        except Exception as e:
            print(e)
    # 熊掌号接入
    @staticmethod
    def baidu_bear_notify(urls):
        try:
            data = '\n'.join(urls)
            result = requests.post(settings.BAIDU_BEAR_NOTIFY_URL, data=data)
            print(result.text)
        except Exception as e:
            print(e)
    # 提交到谷歌
    @staticmethod
    def __google_notify():
        try:
            ping_google('/sitemap.xml')
        except Exception as e:
            print(e)

    @staticmethod
    def notify(url):

        SpiderNotify.baidu_notify(url)
        SpiderNotify.__google_notify()
        SpiderNotify.baidu_bear_notify(url)    