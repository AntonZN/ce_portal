from django.urls import reverse_lazy

EDITOR_I18N = {
    "messages": {
        "ui": {
            "blockTunes": {
                "toggler": {
                    "Click to tune": "Нажмите, чтобы настроить",
                    "or drag to move": "или перетащите",
                },
            },
            "inlineToolbar": {"converter": {"Convert to": "Конвертировать в"}},
            "toolbar": {
                "toolbox": {
                    "Add": "Добавить",
                    "Filter": "Фильтр",
                    "Nothing found": "Ничего не найдено",
                }
            },
        },
        "blockTunes": {
            "delete": {"Delete": "Удалить"},
            "moveUp": {"Move up": "Переместить вверх"},
            "moveDown": {"Move down": "Переместить вниз"},
            "spoiler": {
                "Hide content": "Содержание скрыто",
            },
        },
        "toolNames": {
            "Text": "Параграф",
            "Heading": "Заголовок",
            "List": "Список",
            "Warning": "Примечание",
            "Checklist": "Чеклист",
            "Quote": "Цитата",
            "Code": "Код",
            "Delimiter": "Разделитель",
            "Raw HTML": "HTML-фрагмент",
            "Table": "Таблица",
            "Link": "Ссылка",
            "Marker": "Маркер",
            "Bold": "Полужирный",
            "Italic": "Курсив",
            "InlineCode": "Моноширинный",
            "Image": "Изображение",
        },
    },
    "tools": {
        "warning": {
            "Title": "Название",
            "Message": "Сообщение",
        },
        "link": {"Add a link": "Вставьте ссылку"},
        "stub": {
            "The block can not be displayed correctly.": "Блок не может быть отображен"
        },
        "image": {
            "Upload an image": "Загрузить изображение",
            "Select an Image": "Выберите изображение",
        },
        "list": {
            "Ordered": "Нумерованный",
            "Unordered": "Маркированный",
        },
    },
}

PLUGINS = [
    "@editorjs/paragraph",
    "@editorjs/image@2.6.0",
    "@editorjs/header",
    "@editorjs/list",
    "@editorjs/quote",
    "@editorjs/embed",
    "@editorjs/delimiter",
    # "@editorjs/warning",
    "@editorjs/link",
    "@editorjs/marker",
    "@editorjs/table",
    #"@calumk/editorjs-columns",
    "@weekwood/editorjs-video",
]

EDITORJS_CONFIG_TOOLS = {
    "Image": {
        "class": "ImageTool",
        "inlineToolbar": True,
        "config": {
            "endpoints": {
                "byFile": reverse_lazy("editorjs_image_upload"),
                "byUrl": reverse_lazy("editorjs_image_by_url"),
            }
        },
    },
    "Attaches": {
        "class": "AttachesTool",
        "inlineToolbar": True,
        "buttonText": "Загрузить файл",
        "config": {"endpoint": reverse_lazy("editorjs_file_upload")},
    },
    "Header": {
        "class": "Header",
        "inlineToolbar": True,
        "config": {
            "placeholder": "Enter a header",
            "levels": [2, 3, 4],
            "defaultLevel": 2,
        },
    },
    "List": {"class": "List", "inlineToolbar": True},
    "Quote": {"class": "Quote", "inlineToolbar": True},
    "Embed": {"class": "Embed"},
    "Delimiter": {"class": "Delimiter"},
    "Warning": {"class": "Warning", "inlineToolbar": True},
    "LinkTool": {
        "class": "LinkTool",
        "config": {
            "endpoint": reverse_lazy("editorjs_linktool"),
        },
    },
    "Marker": {"class": "Marker", "inlineToolbar": True},
    "Table": {"class": "Table", "inlineToolbar": True},
}
