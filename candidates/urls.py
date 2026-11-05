from django.urls import path

from .views import (
    candidate_list,
    candidate_create,
    candidate_detail,
    candidate_update,
    candidate_toggle_visibility,
    candidate_delete,
    candidate_trash,
    candidate_restore,
)

app_name = "candidates"

urlpatterns = [
    path(
        "",
        candidate_list,
        name="list",
    ),
    path(
        "new/",
        candidate_create,
        name="create",
    ),
    path("<uuid:pk>/", candidate_detail, name="detail"),
    path("<uuid:pk>/edit/", candidate_update, name="update"),
    path(
        "<uuid:pk>/visibility/",
        candidate_toggle_visibility,
        name="toggle_visibility",
    ),
    path("<uuid:pk>/delete/", candidate_delete, name="delete"),

    path("trash/", candidate_trash, name="trash"),
    path(
        "<uuid:pk>/restore/",
        candidate_restore,
        name="restore",
    ),
]
