from django.contrib import admin

from . models import Post,Comments

class PostModelAdmin(admin.ModelAdmin):

    list_display = ['title','date']
    search_fields = ['title','content']
    #list_editable = ['title']
    class Meta:

        model = Post


class CommentAdmin(admin.ModelAdmin):

    list_display = ['author','content','post']


admin.site.register(Post,PostModelAdmin)
admin.site.register(Comments,CommentAdmin)
