from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.ChatCreateView.as_view(), name='create_chat'),  # создать чат
    path('chats/<int:chat_id>/', views.ChatDetailView.as_view(), name='chat_detail'),  # получить или удалить чат
    path('chats/<int:chat_id>/messages/', views.MessageCreateView.as_view(), name='create_message'),  # создать сообщение
]
