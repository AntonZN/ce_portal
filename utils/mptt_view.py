from django.conf import settings
from django.utils.module_loading import import_string


def _load(module):
    return import_string(module) if isinstance(module, str) else module


class view:
    def __init__(
        self,
        model,
        view,
        slug_field="slug",
        trailing_slash=getattr(settings, "APPEND_SLASH", True),
    ):
        self.model = _load(model)
        self.view = _load(view)
        self.slug_field = slug_field
        self.trailing_slash = trailing_slash

        # define 'get_path' method for model
        self.model.get_path = lambda instance: "/".join(
            [
                getattr(item, slug_field)
                for item in instance.get_ancestors(include_self=True)
            ]
        ) + ("/" if self.trailing_slash else "")

    def __call__(self, *args, **kwargs):
        if "path" not in kwargs:
            raise ValueError(
                "Path was not captured! Please capture it in your urlconf. Example: url(r'^gallery/(?P<path>.*)', mptt_urls.view(...), ...)"
            )

        instance = None  # actual instance the path is pointing to (None by default)
        path = kwargs["path"]
        try:
            instance_slug = path.split("/")[
                -2 if self.trailing_slash else -1
            ]  # slug of the instance
        except IndexError:
            instance_slug = None

        if instance_slug:
            candidates = self.model.objects.filter(
                **{self.slug_field: instance_slug}
            )  # candidates to be the instance
            for candidate in candidates:
                # here we compare each candidate's path to the path passed to this view
                if candidate.get_path() == path:
                    instance = candidate
                    break

        kwargs["instance"] = instance
        return self.view(*args, **kwargs)
