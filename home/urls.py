from django.urls import path

from home.views import *

urlpatterns = [
    path('', Home.as_view(template_name = 'home.html'), name='home'),
    # path('', index, name='home'),
]