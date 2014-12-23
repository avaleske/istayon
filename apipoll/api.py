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

        now = timezone.now()
        #align bin edges to minutes, so for 5 minute intervals, the edges are on the fives.
        bin_edge_difference = (now.minute % INTERVAL_MINUTES) * 60 + now.second
        forward_bin_edge_alignment_offset = (INTERVAL_MINUTES * 60) - bin_edge_difference
        timestamp_start = int(format(now - timedelta(hours=HOURS_BACK), 'U')) - bin_edge_difference

        likes_response = client.blog_likes(settings.TAYLOR_BLOG_URL, after=timestamp_start, limit=1000)
        likes_count = likes_response['liked_count']
        now_unix = int(format(now, 'U'))

        if len(likes_response['liked_posts']) > 0:
            last_liked_time = datetime.utcfromtimestamp(
                likes_response['liked_posts'][0]['liked_timestamp']).replace(tzinfo=pytz.utc)

            timestamps = ((post['liked_timestamp']) for post in likes_response['liked_posts'])

        else:
            last_liked_time = None
            timestamps = [0]

        hist = numpy.histogram(numpy.fromiter(timestamps, int),
                       bins=xrange(now_unix-(HOURS_BACK*60*60)+forward_bin_edge_alignment_offset-(INTERVAL_MINUTES*60),
                                   now_unix+forward_bin_edge_alignment_offset+1,
                                   INTERVAL_MINUTES*60))


        # likes count, histogram, histogram edges
        return likes_count, last_liked_time, hist[0].tolist(), hist[1].tolist()
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