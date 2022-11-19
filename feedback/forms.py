from django import forms
from .models import Feedback, FeedbackForDirector, IdeaFeedback


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ("topic", "type", "text")


class DirectorFeedbackForm(forms.ModelForm):

    class Meta:
        model = FeedbackForDirector
        fields = ("topic", "text")


class IdeaFeedbackForm(forms.ModelForm):

    class Meta:
        model = IdeaFeedback
        fields = ("topic", "text")
