from chat.models import Chatter, Watercooler
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render_to_response
from django.core import serializers
from datetime import timedelta

def index(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Error: Request method must be POST')
    if not 'name' in request.POST:
        return HttpResponseBadRequest('Error: You must provide a username')
    
    return render_to_response('chat.html', { 'user': request.POST['name'] })

def sendMessage(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Error: Request method must be POST')
    if not 'userid' in request.POST or not 'message' in request.POST:
        return HttpResponseBadRequest('Error: You must provide a name and message')
    
    c = Chatter.objects.get(pk=request.POST['userid'])
    w = Watercooler(chatter=c.name, message=request.POST['message'])
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
    
    expiry = timedelta(seconds=30)
    tbr = c.check_in - expiry
    
    u = Chatter.objects.all()
    
    for user in u:
        if tbr > user.check_in:
            user.delete()
    
    serializer = serializers.get_serializer('json')()
    return HttpResponse(serializer.serialize(u))

def init(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Error: Request method must be POST')
    if not 'user' in request.POST:
        return HttpResponseBadRequest('Error: You must provide a state')
    
    c = Chatter(name=request.POST['user'])
    c.save()
    
    return HttpResponse(c.id)
