from django.apps import apps

from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.mixins.section import AppSectionMetaMixin


class SocialSettingsBaseView(AppSectionMetaMixin):
    """ опис спільної поведінки для всіх сторінок
     розділу Налаштування соціальних показників """
    app_label = 'settings'

    def get_section_config(self):
        if not self.app_label:
            raise ValueError("app_label is required")
        return apps.get_app_config(self.app_label)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        for c in ctx:
            print()
            print(f'{c}: {ctx[c]}')
        # ctx['toolbar_buttons'] = self.get_toolbar_buttons()

        return ctx


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
#         {'action': 'views', 'url': 'settings:view_social_settings'},
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
