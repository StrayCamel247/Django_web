

from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait
import multiprocessing
import requests
try:
    from apps.utils.handler import logging_time
except:
    pass
# 线程池
from matrix_factorization.handlers import mf_svds

def mf_svds_handler(params=None):
    #k:'分解矩阵的大小为k*k'
    k = params.get('k')
    res = mf_svds(k)
    return res
    
def hello_word_handler(params=None):
    res = {
        'name': 'stray_camel',
        'age': '25',
        'patient_id': '19000347',
    }
    return res

if __name__ == "__main__":
    mf_svds(20)