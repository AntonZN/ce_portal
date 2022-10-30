from django.shortcuts import render
from django.urls import reverse
from django.utils.functional import cached_property

from django.views.generic import DetailView, ListView
from view_breadcrumbs import BaseBreadcrumbMixin, ListBreadcrumbMixin

from blog.models import News, Category


class CategoryView(BaseBreadcrumbMixin, ListView):
    template_name = "catalog.html"
    model = News
    breadcrumb_use_pk = False
    context_object_name = "category"

    @cached_property
    def crumbs(self):
        return [
            (self.object.name, reverse("catalog:category_detail", kwargs=self.kwargs)),
        ]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get(self, request, slug, sub_slug=None, *args, **kwargs):
        if sub_slug is not None:
            self.object = Category.objects.get(slug=sub_slug)
        else:
            self.object = Category.objects.get(slug=slug)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class NewsListView(ListBreadcrumbMixin, ListView):
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