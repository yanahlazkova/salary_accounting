from django.apps import apps
from ui.buttons.registry import UIButtons


class SectionPageToolbarMixin:
    """ Формує toolbar-кнопки на основі app_icons додатку """

    app_label: str = None
    toolbar_buttons: dict = []  # ['create', 'edit', 'delete']

    def get_app_icons(self) -> dict:
        if not self.app_label:
            return {}

        config = apps.get_app_config(self.app_label)
        return getattr(config, 'app_icons', {}) or {}

    def get_toolbar_buttons(self):
        icons = self.get_app_icons()
        buttons = []

        pk = getattr(self.object, 'pk', None)

        for name in self.toolbar_buttons:
            button = (
                UIButtons(name)
                .set_url_name(self.get_toolbar_url(name))
                .set_pk(pk)
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

        return f'{self.app_label}:{name}'

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
