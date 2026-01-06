from django.urls import path

from home.views import *

urlpatterns = [
    # path('', Home.as_view(), name='home'),
    path('', index, name='home'),
]