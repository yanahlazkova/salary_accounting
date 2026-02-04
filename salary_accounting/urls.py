"""
URL configuration for salary_accounting project.

The `urlpatterns` list routes URLs to view. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function view
    1. Add an import:  from my_app import view
    2. Add a URL to urlpatterns:  path('', view.home, name='home')
Class-based view
    1. Add an import:  from other_app.view import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include

from home.views import pageNotFound

urlpatterns = [
    path('', include('home.urls')),
    path('staff/', include('persons.urls', namespace='personnel')), # кадри
    # path('directories', include('directories.urls')),
    path('settings/', include('settings.urls', namespace='settings')),
    path('admin/', admin.site.urls),
]

handler404 = pageNotFound