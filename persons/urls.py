from django.urls import path

from persons.views import *

urlpatterns = [
    path('/personnel', listpersonnel, name='personnel'),
    # path('/')
]