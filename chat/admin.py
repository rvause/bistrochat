from chat.models import Chatter, Watercooler
from django.contrib import admin

class ChatterAdmin(admin.ModelAdmin):
    list_display = ('name', 'check_in', 'last_message')
    
class WatercoolerAdmin(admin.ModelAdmin):
    list_display = ('time', 'chatter', 'message')
    date_hierarchy = 'time'
    list_filter = ['chatter']
    search_fields = ('message',)
    
admin.site.register(Chatter, ChatterAdmin)
admin.site.register(Watercooler, WatercoolerAdmin)
