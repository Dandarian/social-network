from rest_framework import permissions
import json


class IsOwnerOrReadOnly(permissions.BasePermission):
    # This permission is for the object.
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsNotFanOrReadOnly(permissions.BasePermission):
    # This permission is for the list.
    def has_permission(self, request, view):
        '''Did user already like this post?
        '''
        if request.method in permissions.SAFE_METHODS:
            return True

        body = json.loads(request.body.decode('utf-8'))

        if 'post' in body:
            post_id = body['post']
            likes = view.queryset.filter(post=post_id, owner=request.user)
            # Do not give permission if the like is already exists.
            return not likes.exists()

        return True
