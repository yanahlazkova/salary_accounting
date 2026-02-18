from django.apps import apps
from ui.buttons.registry import UIButtons


class SectionPageToolbarMixin:
    """ Формує toolbar-кнопки на основі app_icons додатку.
     Підтримує pk та slug автоматично. """

    app_label: str = None
    toolbar_buttons: list[str] = []  # ['create', 'edit', 'delete']

    # ------------------------------------------------
    # 🔹 УНІВЕРСАЛЬНЕ визначення kwargs для reverse
    # ------------------------------------------------
    def get_object_url_kwargs(self):
        """ Повертає kwargs для reverse().
        Працює і для pk, і для slug. """

        obj = getattr(self, "object", None)

        if not obj:
            return {}

        # 1️⃣ Якщо використовується slug
        if hasattr(self, "slug_field") and hasattr(self, "slug_url_kwarg"):
            slug_value = getattr(obj, self.slug_field, None)
            if slug_value:
                return {self.slug_url_kwarg: slug_value}

        # 2️⃣ Якщо використовується pk
        if hasattr(obj, "pk"):
            return {"pk": obj.pk}

        return {}

    def get_section_config(self):
        if not self.app_label:
            raise ValueError("app_label is required")
        return apps.get_app_config(self.app_label)

    def get_app_icons(self) -> dict:
        if not self.app_label:
            return {}

        config = self.get_section_config()
        return getattr(config, 'app_icons', {}) or {}

    def get_toolbar_buttons(self):
        icons = self.get_app_icons()
        kwargs = self.get_object_url_kwargs()

        buttons = []

        # pk = getattr(getattr(self, "object", None), "pk", None)

        for name in self.toolbar_buttons:
            button = (
                UIButtons(name)
                .set_url_name(self.get_toolbar_url(name))
                .set_kwargs(kwargs)
                # .set_pk(pk)
                .set_icon(icons.get(name))
                .build()
            )
            buttons.append(button)

        return buttons

    def get_toolbar_url(self, name: str) -> str:
        """ Конвенція імен URL:
               settings:create
               settings:edit
               settings:delete """
        if not self.app_label:
            return '#'
        config = self.get_section_config()
        urls = getattr(config, 'app_urls', {}) or {}
        return f'{self.app_label}:{urls[name]}'

# class SectionPageToolbarMixin:
#     toolbar_buttons = ()
#
#     def get_toolbar_buttons(self):
#         obj = getattr(self, 'object', None)
#         pk = getattr(obj, 'pk', None)
#
#         buttons = []
#         for btn in self.toolbar_buttons:
#             buttons.append(
#                 UIButtons.build(
#                     name=btn['action'],
#                     url_name=btn['url'],
#                     pk=pk,
#                 )
#             )
#         return buttons
