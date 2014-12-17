import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince
from datetime import timedelta
from apipoll import phrases, api, swrcache
from httplib2 import ServerNotFoundError
from django.template import Context


format_string = u"{0} {1}{2}"


#todo do this with a template and divs and pretty
def index(request):
    context = {}
    packed_values = swrcache.get(settings.LIKED_INFO_KEY)
    if not packed_values:
        try:
            packed_values = api.get_like_data()
        except ServerNotFoundError:
            context['message'] = "Something went wrong and we couldn't connect to Tumblr."
            return render(request, 'apipoll/index.html', context)
        swrcache.set(settings.LIKED_INFO_KEY, packed_values, 60)
    count, last_liked, histogram, bins = packed_values

    #todo better this to see if she's coming online, leaving, or has been online for awhile
    if histogram:
        # ramp up
        if histogram[0] > 0 and histogram[1] == 0:
            message = format_string.format(phrases.get_maybe(), phrases.get_name(), phrases.get_maybe_up_end())
        # ramp down
        elif histogram[0] == 0 and histogram[1] > 0:
            message = format_string.format(phrases.get_maybe(), phrases.get_name(), phrases.get_maybe_down_end())
        # online
        elif histogram[0] > 0 and histogram[1] > 0:
            message = format_string.format(phrases.get_yes(), phrases.get_name(), phrases.get_yes_end())
        #offline
        elif sum(histogram[0:2]) == 0:
            message = format_string.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())
    #offline
    else:
        message = format_string.format(phrases.get_no(), phrases.get_name(), phrases.get_no_end())

    context['message'] = message
    context['count'] = count
    context['last_liked'] = last_liked
    context['histogram'] = histogram
    return render(request, 'apipoll/index.html', context)


