from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/constitution/', include('constitution.urls')),
]


# API endpoints: /api/auth/ (register, login, profile) and /api/constitution/ (search, article)
