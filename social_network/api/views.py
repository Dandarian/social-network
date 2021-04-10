from rest_framework import generics, permissions
from . import serializers
from django.contrib.auth.models import User
from .models import Post
from .permissions import IsOwnerOrReadOnly

# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PostList(generics.ListCreateAPIView):
    '''ListCreateAPIView предоставляет распространенный обработчик
    API-методов: get и post для списка.
    '''
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    # IsAuthenticatedOrReadOnly встроен в rest_framework
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        ''' Чтобы при создании указывался авторизованный юзер
        '''
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    '''RetrieveUpdateDestroyAPIView предоставляет распространенный обработчик
    API-методов: get, update и delete для одной сущности.
    '''
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    # IsOwnerOrReadOnly мы создали в файле permissions
    # Здесь нужны оба разрешения, поскольку обновлять или удалять пост должен
    # только залогиненный пользователь, а также его владелец.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
