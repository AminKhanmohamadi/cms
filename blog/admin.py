from django.contrib import admin

from blog.models import Post, Category, Comment


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title' , 'active')
    list_filter = ('active',)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title' , 'category' , 'publish_time' , 'status')
    prepopulated_fields = {'slug':('title',)}
    search_fields = ('title', 'body' , 'lead')
    list_filter = ('status', 'publish_time')
    date_hierarchy = 'publish_time'
    raw_id_fields = ('author',)
    inlines = (CommentInline,)


