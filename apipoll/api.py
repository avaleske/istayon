from django.utils.dateformat import format
import pytz
import numpy
from itertools import groupby
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from httplib2 import ServerNotFoundError
import pytumblr
import logging


def get_like_data():
    log = logging.getLogger(__name__)
    try:
        client = pytumblr.TumblrRestClient(settings.TUMBLR_API_KEY)
        pytumblr.TumblrRestClient.blog_likes = blog_likes_fixed    # replace it with our fixed function

        now = timezone.now()
        # align bin edges to minutes, so for 5 minute intervals, the edges are on the fives.
        # bin_edge_difference is the part from the 5 to the time, like: [5 ### |       10]
        # forward_bin_edge_alignment_offset is the part from the time to the 10, like: [5     | ##### 10]
        bin_edge_difference = (now.minute % settings.INTERVAL_MINUTES) * 60 + now.second
        forward_bin_edge_alignment_offset = (settings.INTERVAL_MINUTES * 60) - bin_edge_difference
        timestamp_start = int(format(
            now - timedelta(hours=settings.HOURS_BACK, minutes=settings.INTERVAL_MINUTES), 'U')) - bin_edge_difference

        log.info("Requesting likes from {0} after {1}, limit {2}".format(settings.TAYLOR_BLOG_URL, timestamp_start, 1000))
        # tumblr's broken at the moment, so commenting this out
        #likes_response = client.blog_likes(settings.TAYLOR_BLOG_URL, after=timestamp_start, limit=1000)
        likes_response = client.blog_likes(settings.TAYLOR_BLOG_URL, limit=1000)
        likes_count = likes_response['liked_count']
        now_unix = int(format(now, 'U'))

        if len(likes_response['liked_posts']) > 0:
            last_liked_time = datetime.utcfromtimestamp(
                likes_response['liked_posts'][0]['liked_timestamp']).replace(tzinfo=pytz.utc)

            timestamps = ((post['liked_timestamp']) for post in likes_response['liked_posts'])

        else:
            last_liked_time = None
            timestamps = [0]

        hist = numpy.histogram(
            numpy.fromiter(timestamps, int),
            bins=xrange(now_unix
                        - (settings.HOURS_BACK*60*60)
                        + forward_bin_edge_alignment_offset
                        - (2*settings.INTERVAL_MINUTES*60),
                        now_unix+forward_bin_edge_alignment_offset+1,
                        settings.INTERVAL_MINUTES*60))

        #set last edge of histogram to now
        hist[1][-1] = now_unix
        # likes count, histogram, histogram edges
        return likes_count, last_liked_time, hist[0].tolist(), hist[1].tolist()
    except ServerNotFoundError:
        return "error"


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