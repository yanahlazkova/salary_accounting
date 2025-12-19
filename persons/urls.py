from django.urls import path

from persons.views import *

urlpatterns = [
    path('/personnel', list_personnel, name='personnel'),
    path('/orders', list_orders, name='orders'),
]