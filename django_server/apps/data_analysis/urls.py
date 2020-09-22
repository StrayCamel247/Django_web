from django.conf.urls import url
from .views import compute_apriori_view
import os
app_name = os.path.dirname(__file__).split('/')[-1].split('\\')[-1]
urlpatterns = [
    url(r'^compute_apriori/$', compute_apriori_view, name='compute_apriori'),
]
