from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like

# REST Framework Django использует сериализаторы, чтобы переводить наборы
# запросов и экземпляры моделей в JSON-данные.

# Сериализатор также создает простые методы create() и update().
# При необходимости их можно переписать.


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'likes']


class UserSerializer(serializers.ModelSerializer):
    # PrimaryKeyRelatedField представляет список публикаций
    # в этом отношении многие-к-одному (many=True указывает
    # на то, что постов может быть больше чем один).
    # Если не задать read_only=True поле posts будет иметь права
    # записи по умолчанию. Это значит, что будет возможность вручную
    # задавать список статей, принадлежащих пользователю при его создании.
    # Вряд ли это желаемое поведение.

    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'posts', 'likes']


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # Мне кажется, что так можно задать, что у каждого лайка один овнер
    # и один пост
    post = serializers.PrimaryKeyRelatedField(many=False, read_only=False)

    class Meta:
        model = Like
        fields = ['id', 'owner', 'post']
