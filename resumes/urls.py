from django.urls import path

from .views import (
    resume_list,
    resume_create,
    resume_detail,
    resume_update,
)


app_name = "resumes"

urlpatterns = [
    path("", resume_list, name="list"),
    path("new/", resume_create, name="create"),
    path(
        "candidate/<uuid:candidate_id>/new/",
        resume_create,
        name="create_for_candidate",
    ),
    path("<uuid:pk>/", resume_detail, name="detail"),
    path("<uuid:pk>/edit/", resume_update, name="update"),
]