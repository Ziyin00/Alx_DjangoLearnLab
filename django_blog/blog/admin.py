from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    list_filter = ('published', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username', 'author__first_name', 'author__last_name')
    list_editable = ('published',)
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Publishing', {
            'fields': ('published',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')