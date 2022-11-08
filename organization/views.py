from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin

from organization.employees.models import Awards


class AwardList(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    template_name = "organization/awards/award_list.html"
    model = Awards
    paginate_by = 15
    context_object_name = "award_list"
    queryset = Awards.objects.all()


class AwardDetail(LoginRequiredMixin, DetailBreadcrumbMixin, DetailView):
    model = Awards
    template_name = "organization/awards/award_detail.html"
    context_object_name = "award"
    breadcrumb_use_pk = True
