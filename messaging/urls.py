from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:recipient_id>/', views.chat, name='chat'),
    path('chat/', views.chat_list, name='chat_list'),
]
