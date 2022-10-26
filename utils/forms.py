from django import forms

from taggit.forms import TagWidget


class TagsAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            "tags": TagWidget(),
        }
