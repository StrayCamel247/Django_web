
import requests
from apps.utils.handler import logging_time
# 线程池
from concurrent.futures import ThreadPoolExecutor,ALL_COMPLETED,wait
import multiprocessing
def hello_word_handler(params=None):
    res = {
            'name': 'stray_camel',
            'age': '25',
            'patient_id': '19000347',
        }
    return res

