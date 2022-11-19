from django.urls import path
from .views import FeedbackView, DirectorFeedbackView, IdeaFeedbackView

app_name = "feedback"

urlpatterns = [
    path(route="", view=FeedbackView.as_view(), name="org_feedback"),
    path(route="director/", view=DirectorFeedbackView.as_view(), name="director_feedback"),
    path(route="idea/", view=IdeaFeedbackView.as_view(), name="idea_feedback"),
]
