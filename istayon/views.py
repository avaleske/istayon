import os
from django.shortcuts import render
from django.http import HttpResponse
import apipoll.models

# Create your views here.
def index(request):
    return HttpResponse("We're still building the stuff to see if she's online. So... maybe? <br />"
                        "She's liked " + str(apipoll.models.get_liked_count()) + " things to date.")
