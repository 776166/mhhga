from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from candidates.models import Candidate
from .forms import ResumeForm
from .models import Resume


@login_required
def resume_list(request):
    resumes = Resume.objects.filter(
        candidate__owner=request.user,
        candidate__is_deleted=False,
    ).select_related("candidate")

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
            Candidate,
            pk=candidate_id,
            owner=request.user,
            is_deleted=False,
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
        Resume.objects.select_related("candidate"),
        pk=pk,
        candidate__owner=request.user,
    )

    return render(
        request,
        "resumes/resume_detail.html",
        {"resume": resume},
    )


@login_required
def resume_update(request, pk):
    resume = get_object_or_404(
        Resume.objects.select_related("candidate"),
        pk=pk,
        candidate__owner=request.user,
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
