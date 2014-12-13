from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.dateformat import format
import pytz
from datetime import datetime
import pytumblr


def get_liked_count():
    client = pytumblr.TumblrRestClient(settings.TUMBLR_API_KEY)
    blog_info = client.blog_info(settings.TAYLOR_BLOG_URL)
    return blog_info['blog']['likes']


def get_new_likes(client=None):
    if not client:
        client = pytumblr.TumblrRestClient(settings.TUMBLR_API_KEY)

    try:
        most_recent_like_time = Like.objects.latest('liked_datetime').liked_datetime
    except ObjectDoesNotExist:
        most_recent_like_time = None

    #get likes
    if most_recent_like_time:
        like_time_as_unix_timestamp = int(format(most_recent_like_time, 'U'))
        likes_response = blog_likes_fixed(client, settings.TAYLOR_BLOG_URL, after=like_time_as_unix_timestamp)
    else:
        likes_response = client.blog_likes(settings.TAYLOR_BLOG_URL, limit=20)

    #save them
    if len(likes_response['liked_posts']) > 0:
        for post in likes_response['liked_posts']:
            post_datetime = datetime.utcfromtimestamp(post['timestamp']).replace(tzinfo=pytz.utc)
            liked_datetime = datetime.utcfromtimestamp(post['liked_timestamp']).replace(tzinfo=pytz.utc)

            l = Like(post_datetime=post_datetime,
                     liked_datetime=liked_datetime,
                     post_url=post['post_url'],
                     post_id=post['id']
                     )
            try:
                l.validate_unique()
                l.save()
            except ValidationError:
                pass


# Fixing the blog_likes() function, because it's broken in the api.
# This can be removed when they merge my pull request in.
def blog_likes_fixed(client, blogname, **kwargs):
    url = "/v2/blog/{0}/likes".format(blogname)
    return client.send_api_request("get", url, kwargs, ['limit', 'offset', 'after', 'before'], True)


class Like(models.Model):
    post_datetime = models.DateTimeField()
    liked_datetime = models.DateTimeField()
    post_url = models.URLField()
    post_id = models.BigIntegerField(unique=True)

class Post(models.Model):
    post_datetime = models.DateTimeField()
    post_url = models.URLField()
    post_id = models.BigIntegerField(unique=True)
