from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Message: чтение и создание.
    'chat' делаем read_only, так как он передаётся из URL/вьюхи.
    """
    class Meta:
        model = Message
        fields = ['id', 'chat', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'chat': {'read_only': True}
        }

    def to_representation(self, instance):
        """
        Кастомное представление для исключения поля chat при необходимости.
        """
        data = super().to_representation(instance)
        # если в контексте явно передан exclude_chat=True, убирает поле chat
        if self.context.get('exclude_chat'):
            data.pop('chat', None)
        return data

    def validate_text(self, value):
        """
        Валидация текста.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Текст сообщения не может быть пустым.")
        if len(value) > 5000:
            raise serializers.ValidationError("Текст сообщения не может превышать 5000 символов.")
        return value


class ChatSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Chat с вложенными сообщениями.
    """
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'title', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        """
        Валидация заголовка.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Заголовок чата не может быть пустым.")
        if len(value) > 200:
            raise serializers.ValidationError("Заголовок чата не может превышать 200 символов.")
        return value
