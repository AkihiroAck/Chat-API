import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from chat.models import Chat, Message


@pytest.mark.django_db
def test_create_chat():
    """
    Отправляет POST-запрос для создания чата и убеждается, что чат создаётся корректно.
    """
    client = APIClient()
    response = client.post(reverse('create_chat'), {'title': 'Test Chat'}, format='json')
    assert response.status_code == 201
    data = response.json()

    # Проверяет, что поле title совпадает и messages — пустой список
    assert data['title'] == 'Test Chat'
    assert data['messages'] == []


@pytest.mark.django_db
def test_create_message():
    """
    Создаёт чат, затем отправляет POST-запрос для создания сообщения в этом чате и убеждается, что сообщение создаётся корректно.
    """
    client = APIClient()
    chat = Chat.objects.create(title='Chat for message')
    url = reverse('create_message', args=[chat.id])
    response = client.post(url, {'text': 'Hello world!'}, format='json')
    assert response.status_code == 201
    data = response.json()

    # Проверяет, что текст сообщения совпадает и нет поля chat
    assert data['text'] == 'Hello world!'
    assert 'chat' not in data


@pytest.mark.django_db
def test_get_chat_with_messages():
    """
    Создаёт чат и несколько сообщений, затем отправляет GET-запрос и убеждается, что возвращаются последние сообщения в нужном порядке.
    """
    client = APIClient()
    chat = Chat.objects.create(title='Chat for get')
    for i in range(5):
        Message.objects.create(chat=chat, text=f'msg {i}')
    url = reverse('chat_detail', args=[chat.id])
    response = client.get(url + '?limit=3')
    assert response.status_code == 200
    data = response.json()

    # Проверяет, что вернулось 3 последних сообщения (по created_at, новые первыми)
    texts = [msg['text'] for msg in data['messages']]
    assert texts == ['msg 4', 'msg 3', 'msg 2']

    # Проверяет, что в сообщениях есть поле chat
    for msg in data['messages']:
        assert 'chat' in msg
        assert msg['chat'] == chat.id


@pytest.mark.django_db
def test_delete_chat():
    """
    Создаёт чат и сообщение, затем отправляет DELETE-запрос и убеждается, что чат и сообщения удаляются.
    """
    client = APIClient()
    chat = Chat.objects.create(title='Chat for delete')
    Message.objects.create(chat=chat, text='to be deleted')
    url = reverse('chat_detail', args=[chat.id])
    response = client.delete(url)
    assert response.status_code == 204

    # Проверяет, что чат и сообщения удалены
    assert not Chat.objects.filter(id=chat.id).exists()
    assert not Message.objects.filter(chat_id=chat.id).exists()
