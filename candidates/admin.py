
from django.contrib import admin

from .models import (
    About,
    Candidate,
    Education,
    Employment,
    EmploymentDescription,
    Skill,
)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "is_visible",
        "is_deleted",
        "created_at",
    )
    list_filter = ("is_visible", "is_deleted")
    search_fields = ("name", "owner__email")
    readonly_fields = ("created_at",)


class CandidateEntryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "candidate",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    search_fields = ("title", "candidate__name")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Education)
class EducationAdmin(CandidateEntryAdmin):
    pass


class EmploymentDescriptionInline(admin.TabularInline):
    model = EmploymentDescription
    extra = 0
    fields = ("title", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Employment)
class EmploymentAdmin(CandidateEntryAdmin):
    inlines = (EmploymentDescriptionInline,)


@admin.register(EmploymentDescription)
class EmploymentDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "employment",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "employment__title",
        "employment__candidate__name",
    )
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Skill)
class SkillAdmin(CandidateEntryAdmin):
    list_display = (
        "title",
        "candidate",
        "level",
        "created_at",
        "updated_at",
    )
    list_filter = ("level", "created_at")


@admin.register(About)
class AboutAdmin(CandidateEntryAdmin):
    pass
