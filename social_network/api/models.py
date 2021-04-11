from django.db import models

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
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'auth.User', related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post', related_name='likes', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
