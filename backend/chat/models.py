from django.db import models


class Chat(models.Model):
    """
    Модель для представления чата.
    """
    title = models.CharField(max_length=200, blank=False)  # заголовок чата
    created_at = models.DateTimeField(auto_now_add=True)  # дата и время создания чата

    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.strip()  # удаление лишних пробелов
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    """
    Модель для представления сообщения в чате.
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')  # связь с чатом
    text = models.CharField(max_length=5000, blank=False)  # текст сообщения
    created_at = models.DateTimeField(auto_now_add=True)  # дата и время создания сообщения

    def save(self, *args, **kwargs):
        if self.text:
            self.text = self.text.strip()  # удаление лишних пробелов
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.chat.title}: {self.text[:50]}"

    class Meta:
        ordering = ['-created_at']
