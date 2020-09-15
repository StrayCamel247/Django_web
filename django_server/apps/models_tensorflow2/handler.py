#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : tensorflow2
# __date__: 2020/09/15 16
import csv
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from openpyxl import Workbook
import io
from django.http import HttpResponse, StreamingHttpResponse, FileResponse


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

# 求fxy的函数值


def fxy(x, y):
    return (x - 10) ** 2 + (y - 10) ** 2


def gradient_descent():
    times = 100  # 迭代次数
    alpha = 0.05  # 步长
    x = 20  # x的初始值
    y = 20  # y的初始值

    fig = Axes3D(plt.figure())      # 将figure转化为3D
    xp = np.linspace(0, 20, 100)
    yp = np.linspace(0, 20, 100)
    xp, yp = np.meshgrid(xp, yp)    # 将数据转化为网格数据
    zp = fxy(xp, yp)
    fig.plot_surface(xp, yp, zp, rstride=1, cstride=1,
                     cmap=plt.get_cmap('rainbow'))

    # 梯度下降算法
    for i in range(times):
        xb = x          # 用于画图
        yb = y          # 用于画图
        fb = fxy(x, y)  # 用于画图

        x = x - alpha * 2 * (x - 10)
        y = y - alpha * 2 * (y - 10)
        f = fxy(x, y)
        print("第%d次迭代：x=%f，y=%f，fxy=%f" % (i + 1, x, y, f))

        fig.plot([xb, x], [yb, y], [fb, f], 'ko', lw=2, ls='-')
    plt.show()


if __name__ == "__main__":
    gradient_descent()
