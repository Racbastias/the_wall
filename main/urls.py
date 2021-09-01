from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('thewall', views.thewall),
    path('publish', views.publish),
    path('comment', views.comment),
    path('deletepublish/<id>', views.deletepublish),
    path('deletecomment/<id>', views.deletecomment),
    path('editpublish/<id>', views.editpublish),
    path('editcomment/<id>', views.editcomment),
    #path('follow/<id>', views.follow),
    #path('unfollow/<id>', views.unfollow),
]
