import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from apipoll.models import BlogInfo, Like, Post

# Create your views here.


def get_liked_count():
    liked_count = cache.get(settings.LIKED_COUNT_KEY)
    if not liked_count:
        liked_count = int(BlogInfo.objects.get(key=settings.LIKED_COUNT_KEY).value)
        # not expiring, since we clear it when we have more info
        cache.set(settings.LIKED_COUNT_KEY, liked_count)
    return liked_count


def get_liked_info():
    liked_info = cache.get(settings.LIKED_INFO_KEY)
    if not liked_info:
        l = Like.objects.latest('liked_datetime')
        sixty = Like.objects.filter(liked_datetime__gte=timezone.now()-timedelta(minutes=60)).count()
        ten = Like.objects.filter(liked_datetime__gte=timezone.now()-timedelta(minutes=10)).count()
        five = Like.objects.filter(liked_datetime__gte=timezone.now()-timedelta(minutes=5)).count()
        liked_info = {'url': l.post_url, 'timestamp': l.liked_datetime, 'five': five, 'ten': ten, 'sixty': sixty}
        # not expiring, since we clear it when we have more info
        cache.set(settings.LIKED_INFO_KEY, liked_info)
    return liked_info


