from django.db import models
from django.conf import settings
import pytumblr


def get_liked_count():
    client = pytumblr.TumblrRestClient(settings.TUMBLR_API_KEY)
    blog_info = client.blog_info(settings.TAYLOR_BLOG_URL)
    return blog_info['blog']['likes']

class BlogEvent(models.Model):
    post_datetime = models.DateTimeField()
    liked_datetime = models.DateTimeField()
    post_url = models.URLField()
    post_id = models.BigIntegerField()