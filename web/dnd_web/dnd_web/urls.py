from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('adventurer/', include('adventurer.urls')),
    path('admin/', admin.site.urls),
]
