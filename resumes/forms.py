from django import forms

from candidates.models import Candidate
from .models import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["candidate", "title", "content"]

    def __init__(self, *args, owner, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["candidate"].queryset = Candidate.objects.filter(
            owner=owner,
            is_deleted=False,
        )

        if candidate is not None:
            self.fields.pop("candidate")

        self.fields["title"].label = "Название"
        self.fields["content"].label = "Текст резюме"
        self.fields["content"].widget = forms.Textarea(
            attrs={"rows": 12}
        )
