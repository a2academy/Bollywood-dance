"""Bollywood DancePro - URL Configuration."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', views.song_library, name='song_library'),
    path('choreographies/', views.choreography_list, name='choreography_list'),
    path('choreographies/<int:pk>/', views.choreography_detail, name='choreography_detail'),
    path('community/', views.community_forum, name='community_forum'),
    path('performances/', views.performance_schedule, name='performance_schedule'),
    path('pricing/', views.pricing, name='pricing'),
    path('about/', views.about, name='about'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
