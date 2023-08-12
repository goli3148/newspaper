from django.contrib import admin
from .models import Article ,Comment
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1 # Extra comment form in article admin

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "body", "author", "slug")
    fields = ("title", "body", "author",)
    inlines = [
        CommentInline,
    ]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)