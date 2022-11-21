from urllib.parse import urlparse

from django import template
from django.db.models import Count
from django.core.exceptions import FieldError
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import resolve

from taggit.models import TaggedItem, Tag
from taggit_templatetags import settings

T_MAX = getattr(settings, "TAGCLOUD_MAX", 6.0)
T_MIN = getattr(settings, "TAGCLOUD_MIN", 1.0)

register = template.Library()


def get_queryset(model):
    queryset = TaggedItem.objects.filter(content_type__app_label=model.lower())
    tag_ids = queryset.values_list("tag_id", flat=True)
    queryset = Tag.objects.filter(id__in=tag_ids)

    try:
        return queryset.annotate(num_times=Count("taggeditem_items"))
    except FieldError:
        return queryset.annotate(num_times=Count("taggit_taggeditem_items"))


@register.simple_tag
def get_taglist(model):
    queryset = get_queryset(model)
    queryset = queryset.order_by("-num_times")
    context = {"tags": queryset}
    return render_to_string(
        template_name="tagify/tag_list.html",
        context=context,
    )


@register.simple_tag
def get_tag_list_for_news(request):
    queryset = get_queryset("Blog")
    url = urlparse(request.get_full_path())
    math = resolve(url.path)
    cat_slug = math.kwargs.get("cat_slug", None)
    active_tag = request.GET.get("tag", None)
    queryset = queryset.order_by("-num_times")
    context = {"tags": queryset, "active_tag": active_tag, "cat_slug": cat_slug}

    return render_to_string(
        template_name="tagify/tag_list_news.html",
        context=context,
    )
