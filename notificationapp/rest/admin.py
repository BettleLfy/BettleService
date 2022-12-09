from django.contrib import admin

from .models import TextingList, Client, Message


admin.site.register(TextingList)
admin.site.register(Client)
admin.site.register(Message)