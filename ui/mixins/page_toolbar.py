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
        return {"pk": obj.pk}

    def get_object_url_kwargs_for(self, obj):
        if not obj:
            return {}

        # 1️⃣ Якщо використовується slug
        if hasattr(self, "slug_field") and hasattr(self, "slug_url_kwarg"):
            slug_value = getattr(obj, self.slug_field, None)
            if slug_value:
                return {self.slug_url_kwarg: slug_value}

        # 2️⃣ Якщо використовується pk
        return {"pk": obj.pk}

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

        for name in self.toolbar_buttons:
            # Назва кнопки не повинна мати знак "_",
            # тому приберемо його, а для url - залишимо
            # button_name = name[: name.find('_')] if name.find('_') != -1 else name
            button_name = name.split("_")[0]
            button = (
                UIButtons(button_name)
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

    def build_toolbar_buttons(self, button_names: list[str], obj=None, extra_kwargs=None):
        icons = self.get_app_icons()

        kwargs = self.get_object_url_kwargs_for(obj) if obj else extra_kwargs

        buttons = []

        for name in button_names:
            button_name = name.split("_")[0]

            button = (
                UIButtons(button_name)
                .set_url_name(self.get_toolbar_url(name))
                .set_kwargs(kwargs)
                .set_icon(icons.get(name))
                .build()
            )
            buttons.append(button)

        return buttons


