from django.apps import apps
from ui.mixins.section import AppSectionMixin


class SocialSettingsBaseView(AppSectionMixin):
    app_label = 'settings'

    page_title = "Налаштування соціальних показників"

    breadcrumbs = {
        'home': {
            'name': 'Home',
            'url': 'home',
        },
        'settings': {
            'name': 'Налаштування',
            # 'url': 'settings:social_settings',
        }
    }

    table_name = 'Соціальні показники'

    toolbar_button = {
        'create': {
            'action': 'create',
            'url': 'settings:create_social_settings',
        },
        'edit': {
            'action': 'edit',
            'url': 'settings:edit_social_settings',
        }, 'view': {
            'action': 'view',
            'url': 'settings:view_social_settings',
        }, 'save': {
            'action': 'save',
            'url': 'settings:save_social_settings',
        }, 'delete': {
            'action': 'delete',
            'url': 'settings:delete_social_settings',
        }, 'exit': {
            'action': 'exit',
            'url': 'settings:social_settings',
        }}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        config = self.get_section_config()

        context['page_title'] = self.page_title
        context['breadcrumbs'] = self.breadcrumbs
        context['toolbar_button'] = self.toolbar_button

        return context
