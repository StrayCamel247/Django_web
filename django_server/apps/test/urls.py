from django.conf.urls import url
from .views import hello_word_view
app_name = 'test'
urlpatterns = [
    url(r'^hello_word/$', hello_word_view.as_view(), name='hello_word'),
]
