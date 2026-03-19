from django.apps import apps
from django.utils import timezone

from settings.forms import SocialSettingsForm
from settings.models import SocialSettings
from ui.mixins.section import AppSectionMetaMixin


class SocialSettingsBaseView(AppSectionMetaMixin):
    """ опис спільної поведінки для всіх сторінок
     розділу Налаштування соціальних показників """
    app_label = 'settings'

    slug_field = "effective_from"
    slug_url_kwarg = "date"

    form_class = SocialSettingsForm
    model = SocialSettings

    form_title: str | None = None

    def get_section_config(self):
        if not self.app_label:
            raise ValueError("app_label is required")
        return apps.get_app_config(self.app_label)

    def get_form_title(self, form_name):
        if form_name == 'create':
            return f'💰 {self.get_page_subtitle(form_name)}'
        elif form_name == 'main':
            return f'💰 {self.get_page_subtitle(form_name)} {timezone.now().year}'
        else:
            return f'💰 {self.get_page_subtitle(form_name)} {self.kwargs[self.slug_url_kwarg]}' # {self.kwargs['date']}'


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
