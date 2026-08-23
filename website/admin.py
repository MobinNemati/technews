from .models import Contact, Newsletter
from django.contrib.admin import ModelAdmin
from django.contrib import admin


class ContactAdmin(ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('name', 'email', 'created_date')
    list_filter = ('email',)
    search_fields = ('name', 'message')



admin.site.register(Contact, ContactAdmin)
admin.site.register(Newsletter)
