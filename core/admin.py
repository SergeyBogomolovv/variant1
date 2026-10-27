from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Feedback, Ticket

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Feedback)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "topic", "priority", "status", "created_at")
    list_filter = ("status", "priority")
    search_fields = ("topic", "description", "user__username")
    list_editable = ("status",)
    list_per_page = 10
