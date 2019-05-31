from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('games/', include('boggle.games.urls')),
    path('admin/', admin.site.urls),
]
