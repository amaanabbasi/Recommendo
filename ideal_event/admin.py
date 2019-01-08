from django.contrib import admin
from .models import User, AppUser, Event, Interest,Interest2,Interest3,KeyVal

admin.site.register(AppUser)
admin.site.register(Event)
admin.site.register(Interest)
admin.site.register(Interest2)
admin.site.register(Interest3)
admin.site.register(KeyVal)