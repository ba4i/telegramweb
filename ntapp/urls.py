from django.urls import path
from . import views

urlpatterns = [
    path('', views.miniapp_view, name='miniapp'),
    path('api/themes/', views.api_themes, name='api_themes'),
    path('api/questions/<int:theme_id>/', views.api_questions, name='api_questions'),
    path('api/save-progress/', views.api_save_progress, name='api_save_progress'),
    path('api/tickets/', views.api_tickets, name='api_tickets'),  # Исправлено имя функции
]
