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
from apipoll import swrcache


log = logging.getLogger(__name__)


def get_like_data_through_cache():
    packed_values = swrcache.get(settings.LIKED_INFO_KEY)
    if not packed_values:
        log.info("liked_info cache miss")
        packed_values = __get_like_data()
        swrcache.set(settings.LIKED_INFO_KEY, packed_values, timeout=60)
    return packed_values


def get_avatar_urls():
    return __get_avatar_url('imstillinbeta'), __get_avatar_url('strangelookonhisface')


def __get_like_data():
    try:
        client = pytumblr.TumblrRestClient(settings.TUMBLR_API_KEY)
        pytumblr.TumblrRestClient.blog_likes = blog_likes_fixed    # replace it with our fixed function

        now = timezone.now()
        # align bin edges to minutes, so for 5 minute intervals, the edges are on the fives.
        # bin_edge_difference is the part from the 5 to the time, like: [2:05 ### |2:07:03|       2:10]
        # forward_bin_edge_alignment_offset is the part from the time to the 10, like: [2:05    |2:07:03| ##### 2:10]
        bin_edge_difference = (now.minute % settings.INTERVAL_MINUTES) * 60 + now.second
        forward_bin_edge_alignment_offset = (settings.INTERVAL_MINUTES * 60) - bin_edge_difference
        timestamp_end = int(format(
            now - timedelta(hours=settings.HOURS_BACK, minutes=settings.INTERVAL_MINUTES), 'U')) - bin_edge_difference

        limit = 50     # but tumblr might be actually limiting at 20...
        offset = 0
        tries = 7
        timestamps = []

        # loop over the likes api call until we have likes from before HOURS_BACK
        # if she likes something between api calls we might have one or two duplicates, it doesn't really matter
        for i in xrange(tries):
            log.info("Requesting likes from {0}, offset {1}, limit {2}".format(settings.TAYLOR_BLOG_URL, offset, limit))
            likes_response = client.blog_likes(settings.TAYLOR_BLOG_URL, offset=offset, limit=limit)
            response_count = len(likes_response['liked_posts'])
            log.info("Got {0} likes".format(response_count))

            offset += response_count
            timestamps.extend((post['liked_timestamp']) for post in likes_response['liked_posts'])

            # if we've gone far enough back, then stop
            if timestamps[-1] < timestamp_end:
                break

        if timestamps:
            last_liked_time = datetime.utcfromtimestamp(timestamps[0]).replace(tzinfo=pytz.utc)
        else:
            timestamps = [0]
            last_liked_time = None

        likes_count = likes_response['liked_count']
        now_unix = int(format(now, 'U'))

        hist = numpy.histogram(
            numpy.fromiter(timestamps, int, count=offset),
            # woo timestamp math. this just makes an iterator that defines where the bin edges should be
            # we start from a safe point before the left edge of the plot and end a safe place in the future
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
    except (ServerNotFoundError, KeyError):
        log.error("Couldn't reach Tumblr.")
        return "error"


def __get_avatar_url(blog_name, size=16):
    cache_key = blog_name + '_AVATAR'
    avatar = swrcache.get(cache_key)
    if not avatar:
        try:
            client = pytumblr.TumblrRestClient(settings.TUMBLR_API_KEY)
            avatar = client.avatar(blog_name, size=size)['avatar_url']
        except ServerNotFoundError:
            avatar = None
        swrcache.set(cache_key, avatar, 60 * 60)
    return avatar


# Fixing the blog_likes() function, because it's broken in the api.
# This can be removed when they merge my pull request in.
def blog_likes_fixed(self, blogname, **kwargs):
    url = "/v2/blog/{0}/likes".format(blogname)
    return self.send_api_request("get", url, kwargs, ['limit', 'offset', 'after', 'before'], True)
