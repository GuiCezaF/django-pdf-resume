from django.contrib import admin
from core.models import Resume


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'is_resumed', 'created_at', 'updated_at')

    fields = ('file_name', 'is_resumed', 'created_at', 'updated_at')


admin.site.register(Resume, ResumeAdmin)
