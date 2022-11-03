from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin

from blog.models import News, Category


class NewsList(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    template_name = "blog/news/list.html"
    model = News
    paginate_by = 12
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