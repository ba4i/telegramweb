# ntapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.miniapp_view, name='miniapp'),
    path('api/tickets/', views.api_tickets, name='api_tickets'),
    path('api/exam-result/', views.api_exam_result, name='api_exam_result'),
    path('api/user-profile/', views.api_user_profile, name='api_user_profile'),
    path('api/leaderboard/', views.api_leaderboard, name='api_leaderboard'),
    path('api/themes/', views.api_themes, name='api_themes'),
]
