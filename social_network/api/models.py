from django.db import models
from django.core.signals import request_started
from django.dispatch import receiver
from django.conf import settings
import jwt
import datetime as DT
from django.utils.timezone import get_current_timezone

# Create your models here.


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey(
        'auth.User', related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


class Like(models.Model):
    created = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(
        'auth.User', related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post', related_name='likes', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


class UserActivity(models.Model):
    last_login = models.DateTimeField()
    last_request = models.DateTimeField()


# Счас каждый запрос перехватывается
@receiver(request_started)
def my_callback(sender, environ, **kwargs):
    print("Request started!")
    print(environ)
    # Из этого запроса берётся jwt токен, если он есть
    if 'HTTP_AUTHORIZATION' in environ:
        token = environ['HTTP_AUTHORIZATION'].split(' ')[1]
        # библиотекой он расшифровывается
        # проверяя сигнатуру
        token_decode = jwt.decode(
            token, settings.SECRET_KEY, algorithms="HS256")
        # определяется юзер айди
        user_id = token_decode['user_id']
        # берём нужного юзера
        user_activity_object = UserActivity.objects.filter(id=user_id)[0]
        # и потом в базу данных записывается время этому юзеру
        user_activity_object.last_request = DT.datetime.now(
            tz=get_current_timezone())
        user_activity_object.save()
