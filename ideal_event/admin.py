from django.contrib import admin
from .models import User, AppUser,Interest,KeyVal

admin.site.register(AppUser)
admin.site.register(Interest)
admin.site.register(KeyVal)