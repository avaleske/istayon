from django.db import models
from django.conf import settings


# leaving these so the django db engine doesn't get confused.

class BlogInfo(models.Model):
    key = models.TextField(unique=True)
    value = models.TextField()


class Like(models.Model):
    post_datetime = models.DateTimeField()
    liked_datetime = models.DateTimeField()
    post_url = models.URLField()
    post_id = models.BigIntegerField(unique=True)


class Post(models.Model):
    post_datetime = models.DateTimeField()
    post_url = models.URLField()
    post_id = models.BigIntegerField(unique=True)
