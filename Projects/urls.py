app_name = 'Projects'

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register, name='register'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('homepage', views.homepage, name = 'homepage'),
    path('projects/new', views.new_project, name = 'new_project')
]