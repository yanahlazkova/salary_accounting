from django.urls import path

from persons.views import *

urlpatterns = [
    path('/personnel/', list_personnel, name='personnel'),
    path('/new_person/', add_person, name='add_person'),
    path('/orders/', list_orders, name='orders'),
    path('new_order/', add_order, name='add_order'),
    path('/personnel/<str:personnel_id>/', edit_personnel, name='edit_personnel'),
    path('/orders/<str:order_id>/', edit_order, name='edit_order'),
]