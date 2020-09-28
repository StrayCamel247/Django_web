# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import profile_view, change_profile_view ,ContactsView ,AddmemberView, DelmemberView ,SearchmemberView,AdminView,users_view
from django.urls import path
# from apps.utils.jwt.views import obtain_jwt_token
app_name='accounts'
urlpatterns = [
    url(r'^profile/$',profile_view,name='profile'),
    url(r'^$',users_view,name='all_users'),
    url(r'^profile/change/$',change_profile_view,name='change_profile'),
    url(r'^contacts/(?P<slug>[\w-]+)/$', ContactsView.as_view(), name='contacts'),
    url(r'^member/del/$', DelmemberView, name='del_member'),
    url(r'^member/add/$', AddmemberView, name='add_member'),
    url(r'^member/search/$', SearchmemberView, name='search_member'),
    url(r'^admin$', AdminView, name='admin'),
]
# urlpatterns +=[
    # path('account/login/', obtain_jwt_token),
# ]