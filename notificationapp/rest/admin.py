from django.contrib import admin

from .models import Client, Message, TextingList

admin.site.register(TextingList)
admin.site.register(Client)
admin.site.register(Message)
