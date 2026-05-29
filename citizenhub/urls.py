from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/constitution/', include('constitution.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]
