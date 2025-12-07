from django.contrib import admin
from django.urls import path, include  # include əlavə et

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authApp.urls')),  # authApp urlslərini çağır
    path('test/', include('psychologyApp.urls')),  # authApp urlslərini çağır
]