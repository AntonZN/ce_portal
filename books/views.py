from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.views.generic import ListView
from view_breadcrumbs import ListBreadcrumbMixin

from books.models import Book


class BooksList(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    template_name = "employees/employee_list.html"
    model = Book
    context_object_name = "books"
    paginate_by = 25

    def get_queryset(self):
        params = self.request.GET
        queryset = Book.objects.all()
        query = params.get("query", None)
        tag = params.get("tag", None)
        if query and not tag:
            query = query.strip()
            queryset = queryset.filter(
                Q(name__icontains=query)
            )

        if tag and not query:
            queryset = queryset.filter(tags__name__in=[tag])

        if tag and query:
            query = query.strip()
            queryset = queryset.filter(
                Q(tags__name__in=[tag])
                & (
                    Q(name__icontains=query)
                )
            )

        page = params.get("page")
        paginator = Paginator(queryset, self.paginate_by)
        queryset = paginator.get_page(page)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = dict()
        queryset = self.get_queryset()
        is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
        context.update({"books": queryset})

        if is_ajax_request:
            html = render_to_string(
                template_name="books/results_partial.html",
                context=context,
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)

        if request.htmx:
            return render(
                request, "books/results_partial.html", context=context
            )

        return render(request, "books/list.html", context=context)
