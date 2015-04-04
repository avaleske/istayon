from datetime import timedelta
import json
import logging
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince
from apipoll import api
from istayon import phrases


MESSAGE_FORMAT_STRING = u"{0} {1}{2}"
TICK_INTERVAL_MINUTES = 15


def index(request):
    log = logging.getLogger(__name__)
    context = {}
    packed_values = api.get_like_data_through_cache()
    if packed_values == "error":
        return render(request, 'istayon/index.html', get_error_context())
    count, last_liked, histogram, bins = packed_values

    imstillinbeta_avatar, strangelookonhisface_avatar = api.get_avatar_urls()

    if histogram:
        # ramp up
        if histogram[-1] > 0 and histogram[-2] == 0:
            message = MESSAGE_FORMAT_STRING.format(phrases.get_maybe(), phrases.get_name(), phrases.get_maybe_up_end())
            context['title'] = "Maybe - IsTayOnTumblr?"
        # ramp down
        elif histogram[-1] == 0 and histogram[-2] > 0:
            message = MESSAGE_FORMAT_STRING.format(phrases.get_maybe(), phrases.get_name(), phrases.get_maybe_down_end())
            context['title'] = "Maybe - IsTayOnTumblr?"
        # online
        elif (histogram[-1] > 0 and histogram[-2] > 0) or sum(histogram[-2:]) > 5:
            message = MESSAGE_FORMAT_STRING.format(phrases.get_yes(), phrases.get_name(), phrases.get_yes_end())
            context['title'] = "Yes! - IsTayOnTumblr?"
        #offline
        elif sum(histogram[-2:]) == 0:
            message = MESSAGE_FORMAT_STRING.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())
            context['title'] = "No - IsTayOnTumblr?"
    #offline
    else:
        message = MESSAGE_FORMAT_STRING.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())
        context['title'] = "No - IsTayOnTumblr?"

    if histogram:
        # I just put the data on the forward edge of the bin, so ignore the first bin edge.
        # at some point maybe I should center it on the bin, but this worked for now.
        context['plot_data'] = map(list, zip(bins[1:], histogram))
        xticks = []
        now_unix = bins[-1]
        start_unix = now_unix - (settings.HOURS_BACK * 60 * 60)
        tick_width = 60 / TICK_INTERVAL_MINUTES
        # define the tick locations on the plot
        # basically, make a list of lists, where each sublist is [tick location, tick text]
        # and if it's not on an hour, then just use an empty string for the text
        for i in xrange(settings.HOURS_BACK * 60 / TICK_INTERVAL_MINUTES + 1):
            xticks.append([start_unix + i * 60 * TICK_INTERVAL_MINUTES,
                           settings.HOURS_BACK-(i/tick_width) if i % tick_width == 0 else ""])
        context['xmin'] = start_unix
        context['xticks'] = json.dumps(xticks)

    context['message'] = message
    context['count'] = count
    # reduce specificity if it's been over six hours since she liked something.
    context['last_liked'] = u"It's been {0} since she liked something.".format(
        timesince(last_liked, timezone.now()) if (timezone.now() - last_liked < timedelta(hours=6))
        else "about " + timesince(last_liked, timezone.now()).split(',')[0])
    context['isib'] = imstillinbeta_avatar
    context['slohf'] = strangelookonhisface_avatar
    return render(request, 'istayon/index.html', context)


def tos(request):
    context = {}
    imstillinbeta_avatar, strangelookonhisface_avatar = api.get_avatar_urls()
    context['isib'] = imstillinbeta_avatar
    context['slohf'] = strangelookonhisface_avatar
    return render(request, 'istayon/tos.html', context)


def get_error_context():
    context = {}
    context['message'] = "Sorry, we had trouble connecting to Tumblr."
    context['count'] = "some"
    context['last_liked'] = "We can't tell when she last liked something, right now."
    context['isib'] = ""
    context['slohf'] = ""
    return context
