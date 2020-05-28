from django.urls import path
from . import views
app_name = 'game'
urlpatterns = [
    path('', views.game),
    path('Snake/', views.snake),
    path('Minesweeper/', views.minesweeper),
]
