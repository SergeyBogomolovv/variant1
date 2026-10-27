from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Feedback, Ticket

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Feedback)
admin.site.register(Ticket)
