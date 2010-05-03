from django.db import models

class Chatter(models.Model):
    name = models.CharField(max_length=20)
    check_in = models.DateTimeField(auto_now_add=True, auto_now=True)
    last_message = models.CharField(max_length=140)
    
class Watercooler(models.Model):
    chatter = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=140)