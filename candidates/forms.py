
from django import forms

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
    class Meta:
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": True,
                }
            ),
        }


class EducationForm(BaseEntryForm):
    class Meta(BaseEntryForm.Meta):
        model = Education


class EmploymentForm(BaseEntryForm):
    class Meta(BaseEntryForm.Meta):
        model = Employment


class SkillForm(BaseEntryForm):
    class Meta(BaseEntryForm.Meta):
        model = Skill
        fields = ["title", "level"]
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
