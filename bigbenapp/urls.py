from django.urls import path
from .views import DetailPostView, CreatePostView
from . import views
from django.shortcuts import reverse

urlpatterns = [
    path('', views.about, name='index'),
    path('book/', views.create_appointment, name='about'),
    path('rdv/', views.rdv, name= "rdv"),
    path('posts/<int:pk>/', DetailPostView.as_view(), name='post-detail'),
    path('post/new/', CreatePostView.as_view(), name='createpost'),
    ]
