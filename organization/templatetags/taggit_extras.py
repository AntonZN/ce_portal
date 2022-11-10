from django import template
from django.db.models import Count
from django.core.exceptions import FieldError
from django.shortcuts import render
from django.template.loader import render_to_string

from taggit.models import TaggedItem, Tag
from taggit_templatetags import settings

T_MAX = getattr(settings, "TAGCLOUD_MAX", 6.0)
T_MIN = getattr(settings, "TAGCLOUD_MIN", 1.0)

register = template.Library()


def get_queryset(applabel):
    queryset = TaggedItem.objects.filter(content_type__app_label=applabel.lower())
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
