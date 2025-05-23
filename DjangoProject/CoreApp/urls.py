from django.contrib import admin
from django.urls import path
from CoreApp import views  # Import views from your app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),  # Admin URL
    path('', views.home, name='home'),  # Home page for login
    path('register/', views.register, name='register'),  # Registration page
    path('Feed/', views.Feed, name='Feed'),  # Feed page
    path('User_Profile/', views.User_Profile, name='User_Profile'),  # User profile page
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # Edit profile page(partial HTMX)
    path('logout/', views.user_logout, name='logout'), # Log out Function Redirecting to the login page
    path('create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
