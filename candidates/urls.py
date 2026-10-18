from django.urls import path

from .views import (
    candidate_list,
    candidate_create,
    candidate_detail,
    candidate_update,
    resume_list,
    resume_create,
    resume_detail,
    resume_update,
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
    path(
        "<int:candidate_id>/",
        candidate_detail,
        name="detail"),
    path(
        "<int:candidate_id>/edit/",
        candidate_update,
        name="update",
    ),
    path(
        "<int:candidate_id>/resumes/",
        resume_list,
        name="resume_list",
    ),
    path(
        "<int:candidate_id>/resumes/new/",
        resume_create,
        name="resume_create",
    ),
    path(
        "<int:candidate_id>/resumes/<int:resume_id>/",
        resume_detail,
        name="resume_detail",
    ),
    path(
        "<int:candidate_id>/resumes/<int:resume_id>/edit/",
        resume_update,
        name="resume_update",
    ),
]
