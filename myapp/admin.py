from django.contrib import admin
from .models import Post, Like, Category, BBS, SEO, Layout


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'description', 'title', 'created_at')
    list_display_links = ('id',)
    ordering = ('-created_at',)
    

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_display_links = ('id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id',)

@admin.register(BBS)
class BBSAdmin(admin.ModelAdmin):
    list_display = ('id', 'bbscontent')
    list_display_links = ('id',)


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)


@admin.register(Layout)
class LayoutAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',) 