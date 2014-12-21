import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince
from datetime import timedelta, datetime
from apipoll import phrases, api, swrcache
from httplib2 import ServerNotFoundError
from django.template import Context
import pytz
import json


format_string = u"{0} {1}{2}"


def index(request):
    context = {}
    packed_values = swrcache.get(settings.LIKED_INFO_KEY)
    if not packed_values:
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
        # ramp down
        elif histogram[-1] == 0 and histogram[-2] > 0:
            message = format_string.format(phrases.get_maybe(), phrases.get_name(), phrases.get_maybe_down_end())
        # online
        elif histogram[-1] > 0 and histogram[-2] > 0:
            message = format_string.format(phrases.get_yes(), phrases.get_name(), phrases.get_yes_end())
        #offline
        elif sum(histogram[-2:]) == 0:
            message = format_string.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())
    #offline
    else:
        message = format_string.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())

    if histogram:
        context['plot_data'] = map(list, zip(bins[1:], histogram))
        # this doesn't work yet...
        context['ticks'] = map(list, zip(bins[-1:], map(
            lambda x: json.dumps(timesince(to_datetime(x), to_datetime(bins[-1]))), bins[1:])))

    context['message'] = message
    context['count'] = "She's liked {0} things.".format(count)
    context['last_liked'] = u"It's been {0} since she liked something.".format(
        "awhile" if last_liked is None else timesince(last_liked, timezone.now()))
    context['isib'] = imstillinbeta_avatar
    context['slohf'] = strangelookonhisface_avatar
    return render(request, 'apipoll/index.html', context)


def to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)