from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('subject', 'user__username')
