from django import forms

from .models import Candidate


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
