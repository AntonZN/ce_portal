from datetime import timedelta

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import get_token

from rest_framework.views import APIView

from organization.models import PhraseDay, PhraseDayLikes


class LikePhrase(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Лайкнуть фразу",
        responses={200: "OK"},
    )
    def post(self, request, phrase_id, *args, **kwargs):
        context = {}

        phrase = PhraseDay.objects.get(id=phrase_id)
        context["phrase"] = phrase
        context["csrf_token"] = get_token(request)

        if PhraseDayLikes.objects.filter(
            employee=request.user, phrase=phrase
        ).exists():
            context["htmx_message"] = "Вы уже голосовали за эту фразу"
        else:
            PhraseDayLikes.objects.create(
                employee=request.user, phrase=phrase
            )
            context["htmx_message"] = "Голос успешно засчитан"


        html = render_to_string(
            template_name="other/phrase_like.html",
            context=context,
        )

        return HttpResponse(html, content_type="text/html")
