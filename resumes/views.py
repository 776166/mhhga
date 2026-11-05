from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from candidates.models import Candidate
from .forms import ResumeForm
from .models import Resume


@login_required
def resume_list(request):
    resumes = (
        Resume.objects
        .for_owner(request.user)
        .active()
        .select_related("candidate")
    )

    return render(
        request,
        "resumes/resume_list.html",
        {"resumes": resumes},
    )


@login_required
def resume_create(request, candidate_id=None):
    candidate = None

    if candidate_id is not None:
        candidate = get_object_or_404(
            Candidate.objects.for_owner(request.user).active(),
            pk=candidate_id,
        )

    if request.method == "POST":
        form = ResumeForm(
            request.POST,
            owner=request.user,
            candidate=candidate,
        )

        if form.is_valid():
            resume = form.save(commit=False)

            if candidate is not None:
                resume.candidate = candidate

            resume.save()

            if candidate is not None:
                return redirect("candidates:detail", pk=candidate.pk)

            return redirect("resumes:list")
    else:
        form = ResumeForm(
            owner=request.user,
            candidate=candidate,
        )

    return render(
        request,
        "resumes/resume_form.html",
        {
            "form": form,
            "candidate": candidate,
        },
    )


@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(
        Resume.objects
        .for_owner(request.user)
        .active()
        .select_related("candidate")
        .select_related("candidate", "about")
        .prefetch_related(
            "education",
            "employment_descriptions__employment",
            "skills",
        ),
        pk=pk,
    )

    employment_groups = []
    groups_by_employment = {}

    descriptions = (
        resume.employment_descriptions
        .select_related("employment")
        .order_by("employment__created_at", "created_at")
    )

    for description in descriptions:
        employment = description.employment

        if employment.pk not in groups_by_employment:
            group = {
                "employment": employment,
                "descriptions": [],
            }
            groups_by_employment[employment.pk] = group
            employment_groups.append(group)

        groups_by_employment[employment.pk]["descriptions"].append(
            description
        )

    return render(
        request,
        "resumes/resume_detail.html",
        {
            "resume": resume,
            "education_entries": resume.education.all(),
            "employment_groups": employment_groups,
            "skill_entries": resume.skills.all(),
            "about_entry": resume.about,
        },
    )


@login_required
def resume_update(request, pk):
    resume = get_object_or_404(
        Resume.objects
        .for_owner(request.user)
        .active()
        .select_related("candidate"),
        pk=pk,
    )

    if request.method == "POST":
        form = ResumeForm(
            request.POST,
            owner=request.user,
            candidate=resume.candidate,
            instance=resume,
        )

        if form.is_valid():
            form.save()
            return redirect("resumes:detail", pk=resume.pk)
    else:
        form = ResumeForm(
            owner=request.user,
            candidate=resume.candidate,
            instance=resume,
        )

    return render(
        request,
        "resumes/resume_form.html",
        {
            "form": form,
            "candidate": resume.candidate,
            "resume": resume,
        },
    )


@login_required
@require_POST
def resume_delete(request, pk):
    resume = get_object_or_404(
        Resume.objects.for_owner(request.user).active(),
        pk=pk,
    )

    resume.soft_delete()
    return redirect("resumes:list")