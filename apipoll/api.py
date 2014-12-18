from django.utils.dateformat import format
import pytz
import numpy
from itertools import groupby
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from httplib2 import ServerNotFoundError
import pytumblr

HOURS_BACK = 2
INTERVAL_MINUTES = 5


def get_like_data():
    try:
        client = pytumblr.TumblrRestClient(settings.TUMBLR_API_KEY)
        pytumblr.TumblrRestClient.blog_likes = blog_likes_fixed    # replace it with our fixed function

        timestamp = int(format(timezone.now() - timedelta(hours=HOURS_BACK), 'U'))
        likes_response = client.blog_likes(settings.TAYLOR_BLOG_URL, after=timestamp, limit=1000)
        likes_count = likes_response['liked_count']

        if len(likes_response['liked_posts']) > 0:
            now = int(format(timezone.now(), 'U'))
            seconds_ago = ((now - post['liked_timestamp']) for post in likes_response['liked_posts'])
            hist = numpy.histogram(numpy.fromiter(seconds_ago, int),
                                   bins=xrange(0, (HOURS_BACK*60*60)+1, INTERVAL_MINUTES*60))

            last_liked_time = datetime.utcfromtimestamp(
                likes_response['liked_posts'][0]['liked_timestamp']).replace(tzinfo=pytz.utc)

            # likes count, histogram, histogram edges
            return likes_count, last_liked_time, hist[0].tolist(), hist[1].tolist()
        return likes_count, None, None, None
    except ServerNotFoundError:
        return "Something went wrong and we couldn't connect to Tumblr."


def get_avatar_url(blog_name, size=16):
    try:
        client = pytumblr.TumblrRestClient(settings.TUMBLR_API_KEY)
        return client.avatar(blog_name, size=size)['avatar_url']
    except ServerNotFoundError:
        return None


# Fixing the blog_likes() function, because it's broken in the api.
# This can be removed when they merge my pull request in.
def blog_likes_fixed(self, blogname, **kwargs):
    url = "/v2/blog/{0}/likes".format(blogname)
    return self.send_api_request("get", url, kwargs, ['limit', 'offset', 'after', 'before'], True)