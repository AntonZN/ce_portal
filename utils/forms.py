from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from utils.tagify.widgets import TagInput


class UserAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "Используйте эту форму для изменения пароля пользователя. "
            '<a href="{}">Изменить пароль</a>.'
        ),
    )
    class Meta:
        widgets = {
            "tags": TagInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format("../password/")
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )

class TagsAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            "tags": TagInput(),
        }