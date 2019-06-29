# -*- coding: utf-8 -*-
# @Author: freen
# @Date:   2019-06-28 12:19:23
# @Last Modified by:   freen
# @Last Modified time: 2019-06-28 12:20:33
from haystack import indexes
from .models import Article

#文件名称必须是 search_indexes.py
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    views = indexes.IntegerField(model_attr='views')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

# Django Haystack: 要想对某个 app 下的数据进行全文检索，就要在该 app 下创建一 search_indexes.py 文件，然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Article），并且继承 SearchIndex 和 Indexable

# 为什么要创建索引？索引就是一本书的目录，可以为读者提供更快速的导航与查找。在这里也是同样的道理，当数据量非常大的时候，若要从这些数据里找出所有的满足搜索条件的几乎是不太可能的，将会给服务器带来极大的负担。所以我们需要为指定的数据添加一个索引（目录），在这里是为 Article 创建一个索引，索引的实现细节是我们不需要关心的，我们只关心为哪些字段创建索引，如何指定

# 每个索引里面必须有且只能有一个字段为 document=True，这代表 django haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)。

# 如果使用一个字段设置了 document=True，则一般约定此字段名为 text，这是在 SearchIndex 类里面一贯的命名，以防止后台混乱，不建议改

# haystack 提供了 use_template=True 在 text 字段中，这样就允许我们使用数据模板去建立搜索引擎索引的文件，就是索引里面需要存放一些什么东西，例如 Article 的 title 字段，这样我们可以通过 title 内容来检索 Article 数据。举个例子，假如你搜索 Python ，那么就可以检索出 title 中含有 Python 的 Article