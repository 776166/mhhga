
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CandidateForm
from .models import Candidate


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
    candidate = get_object_or_404(
        Candidate.objects.for_owner(request.user).active(),
        pk=pk,
    )

    return render(
        request,
        "candidates/candidate_detail.html",
        {
            "candidate": candidate,
            "resumes": candidate.resumes.active(),
        },
    )


@login_required
def candidate_update(request, pk):
    candidate = get_object_or_404(
        Candidate.objects.for_owner(request.user).active(),
        pk=pk,
    )

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
    candidate = get_object_or_404(
        Candidate.objects.for_owner(request.user).active(),
        pk=pk,
    )

    candidate.is_visible = not candidate.is_visible
    candidate.save(update_fields=["is_visible"])

    return redirect("candidates:detail", pk=candidate.pk)


@login_required
@require_POST
def candidate_delete(request, pk):
    candidate = get_object_or_404(
        Candidate.objects.for_owner(request.user).active(),
        pk=pk,
    )

    candidate.soft_delete()
    return redirect("candidates:list")
