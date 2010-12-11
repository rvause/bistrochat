from chat.models import Chatter, Watercooler
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.core import serializers
from datetime import timedelta
from utils import expired_users
import re

USER_WHITELIST = (
    'rvause',
)

CAN_KICK = (
    'rvause',
)


def index(request):
    if not request.method == 'GET':
        return HttpResponseBadRequest('Error: Request method must be POST')
    if not 'name' in request.GET:
        return HttpResponseBadRequest('Error: You must provide a username')
    if not request.GET['name'] in USER_WHITELIST:
        return HttpResponseForbidden('You need a Bistromath account to use the Watercooler')

    return render_to_response('chat.html', { 'user': request.GET['name'] })

def sendMessage(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Error: Request method must be POST')
    if not 'userid' in request.POST or not 'message' in request.POST:
        return HttpResponseBadRequest('Error: You must provide a name and message')
    
    c = Chatter.objects.get(pk=request.POST['userid'])
    if c.name in CAN_KICK and request.POST['message'].startswith('!'):
        kick_user = request.POST['message'][1:]
        if not kick_user in CAN_KICK:
            d = Chatter.objects.get(name=kick_user)
            d.delete()
            w = Watercooler(chatter=c.name, message='*** %s kicked %s ***' % (c.name, kick_user))
            w.save()
            return HttpResponse('Kicked: %s' % request.POST['message'][1:])
    else:
        if request.POST['message'].startswith('/me'):
            message = '*** %s %s' % (c.name, request.POST['message'][4:])
        else:
            message = request.POST['message']

	w = Watercooler(chatter=c.name, message=message)
    	w.save()
    return HttpResponse('Ok')

def updateChat(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Error: Request method must be POST')
    if not 'state' in request.POST:
        return HttpResponseBadRequest('Error: You must provide a state')

    if int(request.POST['state']) == 0:
        set = Watercooler.objects.order_by('time')
        if len(set) > 5:
            set = set[len(set)-5:]
    else:
        set = Watercooler.objects.filter(pk__gt=int(request.POST['state'])).reverse()
    return render_to_response('chat.json', { 'messages': set })

def updateUserlist(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Error: Request method must be POST')
    if not 'userid' in request.POST:
        return HttpResponseBadRequest('Error: You must provide a userid')

    try:
        c = Chatter.objects.get(pk=request.POST['userid'])
    except Chatter.DoesNotExist:
        return HttpResponse('{ "error": "true" }')
    c.save()

    u = expired_users(c)

    serializer = serializers.get_serializer('json')()
    return HttpResponse(serializer.serialize(u))

def init(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Error: Request method must be POST')
    if not 'user' in request.POST:
        return HttpResponseBadRequest('Error: You must provide a state')
        
    c = Chatter.objects.filter(name__exact=request.POST['user']).delete()

    c = Chatter(name=request.POST['user'])
    c.save()
    
    u = expired_users(c)

    return HttpResponse(c.id)

