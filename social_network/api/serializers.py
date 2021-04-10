from rest_framework import serializers
from django.contrib.auth.models import User

# REST Framework Django использует сериализаторы, чтобы переводить наборы
# запросов и экземпляры моделей в JSON-данные.

# Сериализатор также создает простые методы create() и update().
# При необходимости их можно переписать.


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
