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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # config = self.get_section_config()

        context['page_title'] = self.page_title
        context['toolbar_buttons'] = context['toolbar_buttons']
        context['breadcrumbs'] = self.breadcrumbs

        return context
