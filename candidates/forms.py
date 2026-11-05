from django import forms

from resumes.models import Resume

from .models import (
    About,
    Candidate,
    Education,
    Employment,
    EmploymentDescription,
    Skill,
)


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["name"]
        labels = {
            "name": "Имя кандидата",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Имя для идентификации",
                    "autofocus": True,
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError("Укажите имя кандидата.")

        return name


class BaseEntryForm(forms.ModelForm):
    resumes = forms.ModelMultipleChoiceField(
        label="Включить в резюме",
        queryset=Resume.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        fields = ["title", "resumes"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": True,
                }
            ),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)

        # У Employment нет связи с резюме.
        if not hasattr(self.instance, "resumes"):
            self.fields.pop("resumes", None)
            return

        if "resumes" not in self.fields:
            return

        if candidate is not None:
            self.fields["resumes"].queryset = (
                Resume.objects
                .for_owner(candidate.owner)
                .active()
                .filter(candidate=candidate)
            )

        self.fields["resumes"].widget.attrs["class"] = "form-check-input"

        if self.instance.pk:
            self.initial["resumes"] = (
                self.instance.resumes.filter(
                    pk__in=self.fields["resumes"].queryset
                ).values_list("pk", flat=True)
            )


class EducationForm(BaseEntryForm):
    class Meta(BaseEntryForm.Meta):
        model = Education


class EmploymentForm(BaseEntryForm):
    class Meta(BaseEntryForm.Meta):
        model = Employment

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields.pop("resumes")


class SkillForm(BaseEntryForm):
    class Meta(BaseEntryForm.Meta):
        model = Skill
        fields = ["title", "level", "resumes"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": True,
                }
            ),
            "level": forms.Select(
                attrs={"class": "form-select"}
            ),
        }


class AboutForm(BaseEntryForm):
    class Meta(BaseEntryForm.Meta):
        model = About


class EmploymentDescriptionForm(BaseEntryForm):
    class Meta(BaseEntryForm.Meta):
        model = EmploymentDescription

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "Название варианта"
