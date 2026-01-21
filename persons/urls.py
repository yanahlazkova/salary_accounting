from django.urls import path

from persons.views import *

urlpatterns = [
    path('/personnel/', personnel, name='personnel'),
    path('new_person/', add_person, name='add_person'),
    path('orders/', list_orders, name='orders'),
    path('new_order/', add_order, name='add_order'),
    path('personnel/<int:personnel_id>/', edit_personnel, name='edit_personnel'),
    path('orders/<int:order_id>/', edit_order, name='edit_order'),
]