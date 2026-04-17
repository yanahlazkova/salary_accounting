from django.urls import path

from pharmacy import views

from pharmacy.views import PharmacyBasePageView, PharmacyListDrugsView, PharmacyUpdateDB

app_name = 'pharmacy'

urlpatterns = [
    path('', PharmacyBasePageView.as_view(), name='pharmacy'),
    path('search/', PharmacyUpdateDB.as_view(), name='search_drugs'),
    path('update/', PharmacyUpdateDB.as_view(), name='update_db'),
]