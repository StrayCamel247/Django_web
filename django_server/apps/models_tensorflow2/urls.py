from django.conf.urls import url
# from .views import hello_word_view
from apps.models_tensorflow2.DIN_CTR.views import hello_word_view
import os
app_name = os.path.dirname(__file__).split('/')[-1].split('\\')[-1]
urlpatterns = [
    url(r'^hello_word/$', hello_word_view.as_view(), name='hello_word')
]
