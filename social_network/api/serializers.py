from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like, UserActivity

# REST Framework Django uses serializers to translate query sets
# and model instances into JSON data.

# The serializer also creates simple create() and update () methods.
# If necessary, they can be rewritten.


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'likes']


class UserSerializer(serializers.ModelSerializer):
    # PrimaryKeyRelatedField gives
    # many-to-many relation (many=True means
    # that there can be many posts).
    # If you do not set read_only=True, it will be possible to manually
    # set the list of posts that belongs to the user when creating it.
    # This is not the desired behavior.

    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'posts', 'likes']


class UserCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'owner', 'post']


class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserActivity
        fields = ['id', 'last_login', 'last_request']
