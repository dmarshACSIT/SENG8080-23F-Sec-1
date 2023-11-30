from django.contrib import admin
from .models import allAppData
# Register your models here.

class allAppDataAdmin(admin.ModelAdmin):
    search_fields = ("app_name",)
    list_display = ("app_name", "app_category", "app_rating_count", "number_of_downloads", "rated_for")

admin.site.register(allAppData, allAppDataAdmin)
