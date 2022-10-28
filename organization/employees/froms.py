# Django imports
from django import forms
from organization.employees.models import Employee


class EmployeeUpdateForm(forms.ModelForm):
    """
    Creates form for user to update their account.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "name": "email",
                "id": "email",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Employee
        fields = ["fio", "birthday", "username", "email", "avatar"]

        widgets = {
            "fio": forms.TextInput(
                attrs={
                    "name": "fio",
                    "class": "form-control",
                    "id": "fio",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "name": "description",
                    "class": "form-control",
                    "id": "bio",
                    "rows": "5",
                }
            ),
            "birthday": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "id": "birthday",
                    "name": "birthday",
                }
            ),
            "avatar": forms.FileInput(
                attrs={
                    "class": "form-control clearablefileinput",
                    "type": "file",
                    "id": "profileImage",
                }
            ),
        }

