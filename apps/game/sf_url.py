from django.urls import path
from django.views.generic.base import RedirectView
from . import views
import os

urlpatterns = [
    path('', views.street_fighter),
] + [
    path('images/g/' + i, RedirectView.as_view(url='../static/images/g/' + i)) for i in os.listdir(r'static\images\g')
] + [
    path('images/hitEffect/' + i, RedirectView.as_view(url='../static/images/hitEffect/' + i)) for i in os.listdir(r'static\images\hitEffect')
] + [
    path('images/magic/' + i, RedirectView.as_view(url='../static/images/magic/' + i)) for i in os.listdir(r'static\images\magic')
] + [
    path('images/RYU1/' + i, RedirectView.as_view(url='../static/images/RYU1/' + i)) for i in os.listdir(r'static\images\RYU1')
] + [
    path('images/RYU2/' + i, RedirectView.as_view(url='../static/images/RYU2/' + i)) for i in os.listdir(r'static\images\RYU2')
] + [
    path('sound/' + i, RedirectView.as_view(url='../static/sound/' + i)) for i in os.listdir(r'static\sound')
]
