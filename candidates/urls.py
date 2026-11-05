
from django.urls import path

from .views import (
    candidate_list,
    candidate_create,
    candidate_detail,
    candidate_update,
    candidate_toggle_visibility,
    candidate_delete,
    entry_create,
    entry_update,
    entry_delete,
    employment_description_create,
    employment_description_update,
    employment_description_delete,
)

app_name = "candidates"

urlpatterns = [
    path("", candidate_list, name="list"),
    path("new/", candidate_create, name="create"),

    path("<uuid:pk>/", candidate_detail, name="detail"),
    path("<uuid:pk>/edit/", candidate_update, name="update"),
    path(
        "<uuid:pk>/visibility/",
        candidate_toggle_visibility,
        name="toggle_visibility",
    ),
    path("<uuid:pk>/delete/", candidate_delete, name="delete"),

    path(
        "<uuid:candidate_id>/<str:entry_type>/new/",
        entry_create,
        name="entry_create",
    ),
    path(
        "<uuid:candidate_id>/<str:entry_type>/<uuid:pk>/edit/",
        entry_update,
        name="entry_update",
    ),
    path(
        "<uuid:candidate_id>/<str:entry_type>/<uuid:pk>/delete/",
        entry_delete,
        name="entry_delete",
    ),

    path(
        "<uuid:candidate_id>/employment/<uuid:employment_id>/descriptions/new/",
        employment_description_create,
        name="employment_description_create",
    ),
    path(
        "<uuid:candidate_id>/employment/<uuid:employment_id>/descriptions/<uuid:pk>/edit/",
        employment_description_update,
        name="employment_description_update",
    ),
    path(
        "<uuid:candidate_id>/employment/<uuid:employment_id>/descriptions/<uuid:pk>/delete/",
        employment_description_delete,
        name="employment_description_delete",
    ),
]
