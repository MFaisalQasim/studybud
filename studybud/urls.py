"""
URL configuration for studybud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.rooms, name='rooms')
Class-based views
    1. Add an import:  from other_app.views import rooms
    2. Add a URL to urlpatterns:  path('', rooms.as_view(), name='rooms')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "StudyBud Admin"
admin.site.site_title = "StudyBud Admin Portal"
admin.site.index_title = "Welcome to StudyBud Researcher Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
]
