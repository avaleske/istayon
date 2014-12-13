import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince
from datetime import timedelta
from apipoll.models import BlogInfo, Like, Post, refresh_like_data
from apipoll import phrases


format_string = u"{0} {1}{2}"

#todo do this with a template and divs and pretty
def index(request):
    info = get_liked_info()
    if info['five'] > 0 and info['ten'] > 1:
        out = format_string.format(phrases.get_yes(), phrases.get_name(), phrases.get_yes_end())
    elif info['five'] == 0 and info ['ten'] > 0:
        out = format_string.format(phrases.get_maybe(), phrases.get_name(), phrases.get_maybe_end())
    else:
        out = format_string.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())

    out += u"<br /><br />"
    out += u"It's been {0} since she liked something, for a total of {1} likes".format(
        timesince(info['timestamp'], timezone.now()), get_liked_count())
    return HttpResponse(out)


def reload_data(request):
    refresh_like_data()
    return HttpResponse("refreshed data")


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


