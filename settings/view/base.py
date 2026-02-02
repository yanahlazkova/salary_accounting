from ui.buttons.icons import ICONS
from ui.mixins.section import AppSectionMixin


class SocialSettingsBaseView(AppSectionMixin):
    app_label = 'settings'

    page_title = "Налаштування соціальних показників"

    breadcrumbs = {
        'home': {
            'name': 'home',
            'url': 'home',
        },
        'settings': {
            'name': 'Налаштування',
            'url': 'settings',
        }
    }

    table_name = 'Соціальні показники'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = self.page_title
        context['page_icon'] = context['section']['icons']['main']
        # context['toolbar_buttons'] = context['toolbar_buttons']
        context['breadcrumbs'] = self.breadcrumbs

        return context

