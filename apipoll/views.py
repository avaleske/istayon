import os
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince
from datetime import timedelta, datetime
from apipoll import phrases, api, swrcache
import json
import logging


format_string = u"{0} {1}{2}"
TICK_INTERVAL_MINUTES = 20


def index(request):
    log = logging.getLogger(__name__)
    log.debug('starting request')
    context = {}
    packed_values = swrcache.get(settings.LIKED_INFO_KEY)
    if not packed_values:
        log.debug("liked info cache miss")
        print "cache miss"
        packed_values = api.get_like_data()
        swrcache.set(settings.LIKED_INFO_KEY, packed_values, 60)
    count, last_liked, histogram, bins = packed_values

    imstillinbeta_avatar = swrcache.get('ISIB_AVATAR')
    if not imstillinbeta_avatar:
        imstillinbeta_avatar = api.get_avatar_url('imstillinbeta', 16)
        swrcache.set('ISIB_AVATAR', imstillinbeta_avatar, 60*60)

    strangelookonhisface_avatar = swrcache.get('SLOHF_AVATAR')
    if not strangelookonhisface_avatar:
        strangelookonhisface_avatar = api.get_avatar_url('strangelookonhisface', 16)
        swrcache.set('SLOHF_AVATAR', strangelookonhisface_avatar, 60*60)

    if histogram:
        # ramp up
        if histogram[-1] > 0 and histogram[-2] == 0:
            message = format_string.format(phrases.get_maybe(), phrases.get_name(), phrases.get_maybe_up_end())
            context['title'] = "Maybe - IsTayOnTumblr?"
        # ramp down
        elif histogram[-1] == 0 and histogram[-2] > 0:
            message = format_string.format(phrases.get_maybe(), phrases.get_name(), phrases.get_maybe_down_end())
            context['title'] = "Maybe - IsTayOnTumblr?"
        # online
        elif histogram[-1] > 0 and histogram[-2] > 0:
            message = format_string.format(phrases.get_yes(), phrases.get_name(), phrases.get_yes_end())
            context['title'] = "Yes! - IsTayOnTumblr?"
        #offline
        elif sum(histogram[-2:]) == 0:
            message = format_string.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())
            context['title'] = "No - IsTayOnTumblr?"
    #offline
    else:
        message = format_string.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())
        context['title'] = "No - IsTayOnTumblr?"

    if histogram:
        context['plot_data'] = map(list, zip(bins[1:], histogram))
        xticks = []
        now_unix = bins[-1]
        start_unix = now_unix - (settings.HOURS_BACK * 60 * 60)
        tick_width = 60 / TICK_INTERVAL_MINUTES
        for i in xrange(settings.HOURS_BACK * 60 / TICK_INTERVAL_MINUTES + 1):
            xticks.append([start_unix + i * 60 * TICK_INTERVAL_MINUTES,
                           settings.HOURS_BACK-(i/tick_width) if i % tick_width == 0 else ""])
        context['xmin'] = start_unix
        context['xticks'] = json.dumps(xticks)


    context['message'] = message
    context['count'] = "She's liked {0} things.".format(count)
    context['last_liked'] = u"It's been {0} since she liked something.".format(
        "over two hours" if last_liked is None else timesince(last_liked, timezone.now()))
    context['isib'] = imstillinbeta_avatar
    context['slohf'] = strangelookonhisface_avatar
    return render(request, 'apipoll/index.html', context)