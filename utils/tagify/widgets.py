from django import forms
from django.templatetags.static import static


class TagInput(forms.TextInput):
    class Media:
        js = (static("tagify/js/tagify.min.js"),)
        css = {"all": (static("tagify/css/tagify.css"),)}

    template_name = "tagify/tagify_input.html"
    tag_args = {"delimiters": " "}
    var_name = None

    def format_value(self, value):
        if not value:
            return ""
        if isinstance(value, list):
            tags = [tag.name for tag in value]
            return self.tag_args["delimiters"].join(tags)
        return super(TagInput, self).format_value(value)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["type"] = self.input_type
        context["widget"]["tag_args"] = getattr(self, "tag_args", None) or {
            "placeholder": "write some tags",
            "delimiters": ",",
            "pattern": "",
            "whitelist": [],
            "suggestionsMinChars": 1,
            "blacklist": [],
            "maxTags": None,
            "var_name": "",
        }
        return context
