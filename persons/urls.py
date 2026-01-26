from django.urls import path

from persons.views import *

urlpatterns = [
    path('personnel/', personnel, name='personnel'),
    path('new_person/', add_person, name='add_person'),
    path('orders/', list_orders, name='orders'),
    path('new_order/', add_order, name='add_order'),
    path('personnel/<int:pk>/', edit_personnel, name='edit_person'),
    path('orders/<int:pk>/', edit_order, name='edit_order'),
]