from django.contrib import admin
from .models import Post
# Register your models here.

#To be described within iteration 5


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Display in admin panel
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate slugs in admin

admin.site.register(Post, PostAdmin)
