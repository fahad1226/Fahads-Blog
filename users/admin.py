from django.contrib import admin
from .models import Profile

class PostModelAdmin(admin.ModelAdmin):

    list_display = ['user','email']
    search_fields = ['user']
    #list_editable = ['title']
    class Meta:

        model = Profile



admin.site.register(Profile)
