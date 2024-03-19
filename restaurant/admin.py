from django.contrib import admin
from .models import User, Category, Post, Restaurant, Profile, Event

# customize aspects of a post in the admin interface
class PostAdmin(admin.ModelAdmin):
    post_detail = ("id", "user", "content")

class EventAdmin(admin.ModelAdmin):
    list_display= ['start_time', 'end_time', 'description']

# Register your models here.
admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Profile)
admin.site.register(Event, EventAdmin)

