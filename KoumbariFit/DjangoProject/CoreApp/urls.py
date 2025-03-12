from django.contrib import admin
from django.urls import path
from CoreApp import views  # Adjust this import according to your app name

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin page URL
    path('', views.home, name='home'),  # Root path leads to home (login) page
    path('register/', views.register, name='register'),  # Registration page
]
