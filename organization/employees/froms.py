from django import forms
from organization.employees.models import Employee, Contacts


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["fio", "birthday", "description"]
        labels = {
            "description": "О себе",
        }
        widgets = {
            "fio": forms.TextInput(
                attrs={
                    "name": "fio",
                    "class": "form-control",
                    "id": "fio",
                    "readonly": "readonly",
                }
            ),
            "birthday": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "id": "birthday",
                    "name": "birthday",
                    "readonly": "readonly",
                },
            ),
            "description": forms.Textarea(
                attrs={
                    "name": "description",
                    "class": "form-control",
                    "id": "description",
                    "rows": 3,
                }
            ),
        }


class EmployeeContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ["name", "value"]
        exclude = ("id", "employee")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "name": "name",
                    "class": "form-control",
                    "id": "name",
                }
            ),
            "value": forms.TextInput(
                attrs={
                    "name": "value",
                    "class": "form-control",
                    "id": "value",
                }
            ),
        }


EmployeeContactsFormSet = forms.inlineformset_factory(
    Employee, Contacts, form=EmployeeContactsForm, extra=1, max_num=10
)
