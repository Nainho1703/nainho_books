from django.contrib import admin
from .models import UserData

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'data_field', 'created_at')
    search_fields = ('user__username', 'data_field')