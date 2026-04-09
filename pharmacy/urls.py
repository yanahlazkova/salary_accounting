from django.urls import path

from pharmacy import views

from pharmacy.views import PharmacyBasePageView, PharmacyListDrugsView

app_name = 'pharmacy'

urlpatterns = [
    path('', PharmacyBasePageView.as_view(), name='pharmacy'),
    path('search/', PharmacyListDrugsView.as_view(), name='search_drugs'),
]