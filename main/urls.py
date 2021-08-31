from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('thewall', views.thewall),
    path('publish', views.publish)
]
