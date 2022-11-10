from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin

from blog.models import News, Category, NewsLikes


class NewsList(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    template_name = "blog/news/list.html"
    model = News
    paginate_by = 10
    context_object_name = "news_list"
    queryset = News.objects.all()
    ordering = ["-date_published"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            dict(categories=Category.objects.all())
        )
        return context


class NewsDetail(LoginRequiredMixin, DetailBreadcrumbMixin, DetailView):
    model = News
    template_name = "blog/news/detail.html"
    context_object_name = "news"
    breadcrumb_use_pk = False
    slug_url_kwarg = "slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LikeNews(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug, *args, **kwargs):
        context = {}

        news = News.objects.get(slug=slug)
        context["news"] = news
        context["csrf_token"] = get_token(request)

        if NewsLikes.objects.filter(
            employee=request.user, news=news
        ).exists():
            context["htmx_message"] = "Вы уже голосовали за эту новость"
        else:
            NewsLikes.objects.create(
                employee=request.user, news=news
            )
            context["htmx_message"] = "Голос успешно засчитан"


        html = render_to_string(
            template_name="other/news_like.html",
            context=context,
        )

        return HttpResponse(html, content_type="text/html")
