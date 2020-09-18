#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : DIEN论文复现
# __date__: 2020/09/15 16
import csv
from apps.data.handlers import META_ELECTRONICS, REVIEWS_ELECTRONICS_5, TMP_PATH
from apps.constants import MAX_CPUS
from concurrent.futures import (ALL_COMPLETED, ThreadPoolExecutor,
                                as_completed, wait)
import pandas as pd
import numpy as np
import pickle
from openpyxl import Workbook
import io
from apps.api_exception import Fail, ParameterException
import os

def pre_data(params=None):
    params = {'meta': META_ELECTRONICS,
              'reviews': REVIEWS_ELECTRONICS_5}
    file_pathes = params.get('files')
    def json2df(file_path):
        with open(file_path, 'r') as fin:
            df = {}
            i = 0
            for line in fin:
                df[i] = eval(line)
                i += 1
            df = pd.DataFrame.from_dict(df, orient='index')
            return df
    
    reviews_df = json2df(params.get('reviews'))
    with open(os.path.join(TMP_PATH, 'reviews.p'), 'wb') as f:
        pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL)
    
    
    meta_df = json2df(params.get('meta'))
    meta_df = meta_df[meta_df['asin'].isin(reviews_df['asin'].unique())]
    meta_df = meta_df.reset_index(drop=True)
    with open(os.path.join(TMP_PATH, 'meta.p'), 'wb') as f:
        pickle.dump(meta_df, f, pickle.HIGHEST_PROTOCOL)

    

def hello_word_handler(params=None):
    res = {
        'name': 'stray_camel',
        'age': '25',
        'patient_id': '19000347',
    }
    return res


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C',
                     '"Testing"', "Here's a quote"])
    return response


def some_streaming_csv_view(params=None):
    """"A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response


def get_amazon_data(params):
    # with open(REVIEWS_ELECTRONICS_5, 'r') as fin:
    #     df = {}
    #     i = 0
    # with ThreadPoolExecutor(MAX_CPUS) as executor:
    #     for line in fin:
    #         df[i] = eval(line)
    #         i += 1
    # df = pd.DataFrame.from_dict(df, orient='index')
    # return df

    df = pd.read_json(REVIEWS_ELECTRONICS_5, orient='values', encoding='utf-8')
    with open(TMP_PATH, 'wb') as f:
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
