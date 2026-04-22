from django.urls import path

from pharmacy import views

from pharmacy.views import PharmacyBasePageView, PharmacyListDrugsView, PharmacyUpdateDrugsDB, PharmacyUpdateCategory

app_name = 'pharmacy'

urlpatterns = [
    path('', PharmacyBasePageView.as_view(), name='pharmacy'),
    path('search/', PharmacyUpdateDrugsDB.as_view(), name='search_drugs'),
    path('update/', PharmacyUpdateCategory.as_view(), name='update_categories'),
]