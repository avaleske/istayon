import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince
from datetime import timedelta
from apipoll import phrases, api, swrcache


format_string = u"{0} {1}{2}"


#todo do this with a template and divs and pretty
def index(request):

    packed_values = swrcache.get(settings.LIKED_INFO_KEY)
    if not packed_values:
        packed_values = api.get_like_data()
        swrcache.set(settings.LIKED_INFO_KEY, packed_values, 60)
    count, last_liked, histogram, bins = packed_values

    if histogram:
        if histogram[0] > 0 and histogram[1] > 1:
            out = format_string.format(phrases.get_yes(), phrases.get_name(), phrases.get_yes_end())
        elif histogram[0] == 0 and histogram[1] > 0:
            out = format_string.format(phrases.get_maybe(), phrases.get_name(), phrases.get_maybe_end())
        else:
            out = format_string.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())
    else:
        out = format_string.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())

    out += u"<br /><br />"
    out += u"It's been {0} since she liked something, for a total of {1} likes".format(
        "awhile" if last_liked is None else timesince(last_liked, timezone.now()), count)
    return HttpResponse(out)


