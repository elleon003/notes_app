from django.contrib import admin
from .models import Idea, Category, Tag

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'user', 'category', 'start_date', 'due_date', 'created_at')
    list_filter = ('category', 'tags', 'start_date', 'due_date', 'created_at')
    search_fields = ('content', 'side_notes', 'user__email')
    autocomplete_fields = ['user', 'category', 'tags']
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tags',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content > 50)else obj.content
    content_preview.short_description = 'Content'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

