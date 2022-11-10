from django import forms

from utils.tagify.widgets import TagInput


class TagsAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            "tags": TagInput(),
        }
