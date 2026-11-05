
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    AboutForm,
    CandidateForm,
    EducationForm,
    EmploymentDescriptionForm,
    EmploymentForm,
    SkillForm,
)
from .models import Candidate


ENTRY_TYPES = {
    "education": ("education_entries", EducationForm, "Образование"),
    "employment": ("employment_entries", EmploymentForm, "Место работы"),
    "skill": ("skill_entries", SkillForm, "Навык"),
    "about": ("about_entries", AboutForm, "О себе"),
}


def get_candidate(user, candidate_id):
    return get_object_or_404(
        Candidate.objects.for_owner(user).active(),
        pk=candidate_id,
    )


def get_entry_config(entry_type):
    config = ENTRY_TYPES.get(entry_type)

    if config is None:
        raise Http404

    return config


@login_required
def candidate_list(request):
    queryset = Candidate.objects.for_owner(request.user).active()
    candidates = Paginator(queryset, 25).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "candidates/candidate_list.html",
        {"candidates": candidates},
    )


@login_required
def candidate_create(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)

        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.owner = request.user
            candidate.save()
            return redirect("candidates:list")
    else:
        form = CandidateForm()

    return render(
        request,
        "candidates/candidate_form.html",
        {"form": form},
    )


@login_required
def candidate_detail(request, pk):
    candidate = get_candidate(request.user, pk)

    return render(
        request,
        "candidates/candidate_detail.html",
        {
            "candidate": candidate,
            "resumes": candidate.resumes.active(),
            "education_entries": candidate.education_entries.all(),
            "employment_entries": (
                candidate.employment_entries.prefetch_related("descriptions")
            ),
            "skill_entries": candidate.skill_entries.all(),
            "about_entries": candidate.about_entries.all(),
        },
    )


@login_required
def candidate_update(request, pk):
    candidate = get_candidate(request.user, pk)

    if request.method == "POST":
        form = CandidateForm(request.POST, instance=candidate)

        if form.is_valid():
            form.save()
            return redirect("candidates:detail", pk=candidate.pk)
    else:
        form = CandidateForm(instance=candidate)

    return render(
        request,
        "candidates/candidate_form.html",
        {
            "form": form,
            "candidate": candidate,
        },
    )


@login_required
@require_POST
def candidate_toggle_visibility(request, pk):
    candidate = get_candidate(request.user, pk)

    candidate.is_visible = not candidate.is_visible
    candidate.save(update_fields=["is_visible"])

    return redirect("candidates:detail", pk=candidate.pk)


@login_required
@require_POST
def candidate_delete(request, pk):
    candidate = get_candidate(request.user, pk)
    candidate.soft_delete()

    return redirect("candidates:list")


@login_required
def entry_create(request, candidate_id, entry_type):
    candidate = get_candidate(request.user, candidate_id)
    related_name, form_class, title = get_entry_config(entry_type)

    if request.method == "POST":
        form = form_class(request.POST)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.candidate = candidate
            entry.save()

            return redirect("candidates:detail", pk=candidate.pk)
    else:
        form = form_class()

    return render(
        request,
        "candidates/candidate_enty_form.html",
        {
            "form": form,
            "candidate": candidate,
            "title": f"Добавить: {title.lower()}",
        },
    )


@login_required
def entry_update(request, candidate_id, entry_type, pk):
    candidate = get_candidate(request.user, candidate_id)
    related_name, form_class, title = get_entry_config(entry_type)

    entry = get_object_or_404(
        getattr(candidate, related_name),
        pk=pk,
    )

    if request.method == "POST":
        form = form_class(request.POST, instance=entry)

        if form.is_valid():
            form.save()
            return redirect("candidates:detail", pk=candidate.pk)
    else:
        form = form_class(instance=entry)

    return render(
        request,
        "candidates/candidate_enty_form.html",
        {
            "form": form,
            "candidate": candidate,
            "title": f"Редактировать: {title.lower()}",
            "entry": entry,
        },
    )


@login_required
@require_POST
def entry_delete(request, candidate_id, entry_type, pk):
    candidate = get_candidate(request.user, candidate_id)
    related_name, form_class, title = get_entry_config(entry_type)

    entry = get_object_or_404(
        getattr(candidate, related_name),
        pk=pk,
    )
    entry.delete()

    return redirect("candidates:detail", pk=candidate.pk)


@login_required
def employment_description_create(
    request,
    candidate_id,
    employment_id,
):
    candidate = get_candidate(request.user, candidate_id)
    employment = get_object_or_404(
        candidate.employment_entries,
        pk=employment_id,
    )

    if request.method == "POST":
        form = EmploymentDescriptionForm(request.POST)

        if form.is_valid():
            description = form.save(commit=False)
            description.employment = employment
            description.save()

            return redirect("candidates:detail", pk=candidate.pk)
    else:
        form = EmploymentDescriptionForm()

    return render(
        request,
        "candidates/candidate_enty_form.html",
        {
            "form": form,
            "candidate": candidate,
            "title": "Добавить вариант описания",
            "parent": employment,
        },
    )


@login_required
def employment_description_update(
    request,
    candidate_id,
    employment_id,
    pk,
):
    candidate = get_candidate(request.user, candidate_id)
    employment = get_object_or_404(
        candidate.employment_entries,
        pk=employment_id,
    )
    description = get_object_or_404(
        employment.descriptions,
        pk=pk,
    )

    if request.method == "POST":
        form = EmploymentDescriptionForm(
            request.POST,
            instance=description,
        )

        if form.is_valid():
            form.save()
            return redirect("candidates:detail", pk=candidate.pk)
    else:
        form = EmploymentDescriptionForm(instance=description)

    return render(
        request,
        "candidates/candidate_enty_form.html",
        {
            "form": form,
            "candidate": candidate,
            "title": "Редактировать вариант описания",
            "parent": employment,
            "entry": description,
        },
    )


@login_required
@require_POST
def employment_description_delete(
    request,
    candidate_id,
    employment_id,
    pk,
):
    candidate = get_candidate(request.user, candidate_id)
    employment = get_object_or_404(
        candidate.employment_entries,
        pk=employment_id,
    )
    description = get_object_or_404(
        employment.descriptions,
        pk=pk,
    )
    description.delete()

    return redirect("candidates:detail", pk=candidate.pk)
