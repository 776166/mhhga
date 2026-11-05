
from django.contrib import admin

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "candidate",
        "is_deleted",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_deleted", "created_at")
    search_fields = ("title", "candidate__name")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
