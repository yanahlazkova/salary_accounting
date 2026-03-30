from django.urls import path

from pharmacy import views
from pharmacy.views import PharmacyView

app_name = 'pharmacy'

urlpatterns = [
    path('', PharmacyView.as_view(), name='pharmacy'),
]