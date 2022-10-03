"""URL patterns for users app"""

from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    # include authorization URL dy default
    path('', include('django.contrib.auth.urls')),
    # users page
    path('register/', views.register, name='register'),
]


