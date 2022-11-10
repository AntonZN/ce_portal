from functools import cached_property

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DetailView, ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin

from blog.models import News, Category, NewsLikes


class NewsList(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    template_name = "blog/news/list.html"
    model = News
    paginate_by = 10
    context_object_name = "news_list"
    ordering = ["-date_published"]

    def get_queryset(self):
        cat_slug = self.kwargs.get("cat_slug", None)
        if cat_slug:
            return News.objects.filter(category__slug=cat_slug)
        return News.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context.update(
            dict(categories=Category.objects.all(), active_cat=self.kwargs.get("cat_slug"))
        )
        return context


class NewsDetail(LoginRequiredMixin, DetailBreadcrumbMixin, DetailView):
    model = News
    template_name = "blog/news/detail.html"
    context_object_name = "news"
    breadcrumb_use_pk = False
    slug_url_kwarg = "slug"

    @cached_property
    def crumbs(self):
        category_kwargs = self.kwargs.copy()
        del category_kwargs["slug"]
        return [
            (
                self.object.category,
                reverse("blog:news_list", kwargs=category_kwargs),
            ),
            (self.object.title, reverse("blog:news_detail", kwargs=self.kwargs)),
        ]

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
