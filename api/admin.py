from django.contrib import admin

from .models import User, Client, Occupation, Agent, Ticket

# Register your models here.

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Occupation)
admin.site.register(Agent)
admin.site.register(Ticket)