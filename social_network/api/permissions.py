from rest_framework import permissions
import json


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsNotFanOrReadOnly(permissions.BasePermission):
    # Поскольку используется со списком, то не has_object_permission, а
    def has_permission(self, request, view):
        '''Проверяет, лайкал ли уже этот юзер этот пост
        '''
        if request.method in permissions.SAFE_METHODS:
            return True

        post = json.loads(request.body.decode('utf-8'))['post']
        # Фильтруем по посту и юзеру
        likes = view.queryset.filter(post=post, owner=request.user)
        # Не выдаём разрешения, если лайк уже поставлен
        return not likes.exists()
