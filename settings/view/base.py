from django.apps import apps
from ui.mixins.section import AppSectionMixin


class SocialSettingsBaseView(AppSectionMixin):
    """ опис спільної поведінки для всіх сторінок
     розділу Налаштування соціальних показників """
    app_label = 'settings'

    # назви розділів
    page_title = "Налаштування соціальних показників"

    all_page = {
        'home': {
            'name': 'Home',
            'url': 'home',
        },
        'social_settings': {
            'name': 'Налаштування',
            'url': 'settings:social_settings',
        },
        'create_social_settings': {
            'name': 'Додавання нових налаштувань',
            'url': 'settings:create_social_settings',
        },
        'edit_social_settings': {
            'name': 'Редагування налаштувань за ',
            'url': 'settings:edit_social_settings',
        },
        'view_social_settings': {
            'name': 'Перегляд налаштувань за ',
            'url': 'settings:view_social_settings',
        },
    }

    table_name = 'Соціальні показники'

    toolbar_button = {
        'create': {
            'action': 'create',
            'url': 'settings:create_social_settings'
        },
        'edit': {
            'action': 'edit',
            'url': 'settings:create_social_settings',
        },
        'view': {
            'action': 'view',
            'url': 'settings:edit_social_settings',
        },
        'save': {
            'action': 'save',
            'url': 'settings:view_social_settings',
        },
        'delete': {
            'action': 'delete',
            'url': 'settings:save_social_settings',
        },
        'exit': {
            'action': 'exit',
            'url': 'settings:delete_social_settings',
        }
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        config = self.get_section_config()

        context['page_title'] = self.page_title
        context['all_page'] = self.all_page
        context['table_name'] = self.table_name
        context['toolbar_button'] = self.toolbar_button

        return context


class AnotherSettingsBaseView(AppSectionMixin):
    """ опис спільної поведінки для всіх сторінок
     розділу Інші налаштування """
    app_label = 'another'

    # назви розділів
    page_title = 'Інші налаштування'

    breadcrumbs = {
        'home': {
            'name': 'Home',
            'url': 'home',
        },
        'another': {
            'name': 'Інші налаштування',
            'url': 'settings:another_settings',
        }
    }

    table_name = 'Інші налаштування'

    toolbar_button = {
        'create': {
            'action': 'create',
            'url': 'settings:create_another_settings',
        },

    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        config = self.get_section_config()

        context['section'] = config
        context['page_title'] = self.page_title
        context['breadcrumbs'] = self.breadcrumbs
        context['table_name'] = self.table_name
        context['toolbar_button'] = self.toolbar_button

        return context