from django.contrib import admin
from django.urls import path, include
import rest.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(rest.urls))
]
