from django.apps import apps

from ui.buttons.registry import UIButtons
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.mixins.section import AppSectionMixin


class SocialSettingsBaseView(AppSectionMixin, SectionPageToolbarMixin):
    """ опис спільної поведінки для всіх сторінок
     розділу Налаштування соціальних показників """
    app_label = 'settings'

    # назви розділів
    page_title = "Налаштування соціальних показників"

    # all_page = {
    #     'home': {
    #         'name': 'Home',
    #         'url': 'home',
    #     },
    #     'social_settings': {
    #         'name': 'Налаштування',
    #         'url': 'settings:social_settings',
    #     },
    #     'create_social_settings': {
    #         'name': 'Додавання нових налаштувань',
    #         'url': 'settings:create_social_settings',
    #     },
    #     'edit_social_settings': {
    #         'name': 'Редагування налаштувань за ',
    #         'url': 'settings:edit_social_settings',
    #     },
    #     'view_social_settings': {
    #         'name': 'Перегляд налаштувань за ',
    #         'url': 'settings:view_social_settings',
    #     },
    # }

    table_name = 'Соціальні показники'

    # toolbar_buttons = (
    #     {'action': 'create', 'url': 'settings:create_social_settings'},
    #     {'action': 'edit', 'url': 'settings:create_social_settings'},
    #     {'action': 'view', 'url': 'settings:edit_social_settings'},
    #     {'action': 'save', 'url': 'settings:view_social_settings'},
    #     {'action': 'delete', 'url': 'settings:save_social_settings'},
    #     {'action': 'exit', 'url': 'settings:delete_social_settings'}
    # )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # config = self.get_section_config()

        context['page_title'] = self.page_title
        context['table_name'] = self.table_name

        return context


# class AnotherSettingsBaseView(AppSectionMixin):
#     """ опис спільної поведінки для всіх сторінок
#      розділу Інші налаштування """
#     app_label = 'another'
#
#     # назви розділів
#     page_title = 'Інші налаштування'
#
#     breadcrumbs = {
#         'home': {
#             'name': 'Home',
#             'url': 'home',
#         },
#         'another': {
#             'name': 'Інші налаштування',
#             'url': 'settings:another_settings',
#         }
#     }
#
#     table_name = 'Інші налаштування'
#
#     toolbar_buttons = (
#         {'action': 'create', 'url': 'settings:create_social_settings'},
#         {'action': 'edit', 'url': 'settings:edit_social_settings'},
#         {'action': 'view', 'url': 'settings:view_social_settings'},
#         {'action': 'save', 'url': 'settings:save_social_settings'},
#         {'action': 'delete', 'url': 'settings:delete_social_settings'},
#         {'action': 'exit', 'url': 'settings:exit_social_settings'}
#     )
#
#     def get_toolbar_buttons(self, pk=None):
#         return [
#             UIButtons.build(
#                 name=btn['action'],
#                 url_name=btn['url'],
#                 pk=pk,
#             )
#             for btn in self.toolbar_buttons
#         ]
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         config = self.get_section_config()
#
#         context['section'] = config
#         context['page_title'] = self.page_title
#         context['breadcrumbs'] = self.breadcrumbs
#         context['table_name'] = self.table_name
#         # context['toolbar_buttons'] = self.get_toolbar_buttons(pk=getattr(self.toolbar_buttons, 'pk', None))
#
#         return context
