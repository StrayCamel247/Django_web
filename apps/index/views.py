from django.shortcuts import render
from django.views import generic
from django.conf import settings
from .models import FriendLink
# Create your views here.
class IndexView(generic.ListView):
    model = FriendLink
    template_name = 'index.html'
    context_object_name = 'test'