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
        limit = 500     # but tumblr might be actually limiting at 50...
        tries = 7
        timestamps = []

        # make at most "tries" tries at getting her likes. We limit it so if she likes stuff between loops it won't go forever
        # this basically always results in an extra api call with no likes, which is sucky.
        for i in xrange(tries):
            log.info("Requesting likes from {0}, after {1}, limit {2}".format(settings.TAYLOR_BLOG_URL, timestamp_start, limit))
            likes_response = client.blog_likes(settings.TAYLOR_BLOG_URL, after=timestamp_start, limit=limit)
            log.info("Got {0} likes".format(len(likes_response['liked_posts'])))

            if len(likes_response['liked_posts']) > 0:
                last_liked_time = datetime.utcfromtimestamp(
                    likes_response['liked_posts'][0]['liked_timestamp']).replace(tzinfo=pytz.utc)
                timestamps.extend((post['liked_timestamp']) for post in likes_response['liked_posts'])
                timestamp_start = likes_response['liked_posts'][0]['liked_timestamp']

            else:
                break

        if not timestamps:
            timestamps = [0]
            last_liked_time = None

        likes_count = likes_response['liked_count']
        now_unix = int(format(now, 'U'))

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
        hist_data = hist[0].tolist()
        hist_edeges = hist[1].tolist()
        # likes count, histogram, histogram edges
        log.info("like results: {0} {1} {2} {3}".format(likes_count, last_liked_time, hist_data, hist_edeges))
        return likes_count, last_liked_time, hist_data, hist_edeges
    except ServerNotFoundError:
        log.error("Couldn't reach Tumblr.")
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
