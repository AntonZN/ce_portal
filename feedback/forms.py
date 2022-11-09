from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ("topic", "type", "text")


class DirectorFeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ("topic", "text")
