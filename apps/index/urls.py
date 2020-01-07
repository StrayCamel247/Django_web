from django.conf.urls import url
from .views import IndexView
app_name='blog'
urlpatterns = [
    # 首页
    url(r'^$', IndexView.as_view(template_name='index.html'), name='index'),  # 主
]
