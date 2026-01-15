from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from chat.logger import log
from .models import Chat
from .serializers import (
    ChatSerializer,
    MessageSerializer
)


class ChatCreateView(APIView):
    """
    POST /chats/ — создать чат
    Body: {"title": "string"}
    """
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            chat = serializer.save()
            log(f"Создан чат: title={chat.title[:50]} id={chat.id}", save=True)
            return Response(
                ChatSerializer(chat).data,
                status=status.HTTP_201_CREATED
            )
        log(f"Ошибка создания чата: {serializer.errors}", save=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatDetailView(APIView):
    """
    GET /chats/{id} — получить чат и последние N сообщений
    Query: limit (по умолчанию 20, максимум 100)
    
    DELETE /chats/{id} — удалить чат вместе со всеми сообщениями
    Response: 204 No Content
    """
    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        
        # получить limit из query параметров
        limit = request.query_params.get('limit', 20)
        try:
            limit = int(limit)
            if limit > 100:
                limit = 100
            elif limit < 1:
                limit = 20
        except (ValueError, TypeError):
            limit = 20
        
        # получить последние N сообщений
        messages = chat.messages.all()[:limit]
        
        # формирует ответ
        serializer = ChatSerializer(chat)
        data = serializer.data
        # заменяет все сообщения на последние N
        data['messages'] = MessageSerializer(messages, many=True).data
        
        return Response(data)
    
    def delete(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        log(f"Удаляет чат {chat.title[:50]}[{chat.id}] и все связанные сообщения", save=True)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageCreateView(APIView):
    """
    POST /chats/{id}/messages/ — отправить сообщение в чат
    Body: {"text": "string"}
    """
    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(chat=chat)
            # флаг exclude_chat убирает поле chat из ответа
            data = MessageSerializer(message, context={'exclude_chat': True}).data
            log(f"Создано сообщение {message.text[:50]}[{message.id}] в чате {chat.title[:50]}[{chat.id}]", save=True)
            return Response(
                data,
                status=status.HTTP_201_CREATED
            )
        log(f"Ошибка создания сообщения в чате {chat.title[:50]}[{chat.id}]: {serializer.errors}", save=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
