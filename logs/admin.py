from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'path', 'method', 'timestamp')
    list_filter = ('user', 'method', 'timestamp')
    search_fields = ('user__username', 'path')
    ordering = ('-timestamp',)
