import os
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    times = int(os.environ.get('TIMES',3))
    boolean = bool(os.environ.get('TESTTEST', True))
    return HttpResponse(str(boolean) + 'Hello! ' * times )