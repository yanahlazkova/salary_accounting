from django.apps import apps
from ui.mixins.section import AppSectionMixin


class SocialSettingsBaseView(AppSectionMixin):
    """ опис спільної поведінки для всіх сторінок додатка """
    app_label = 'settings'

    # назви розділів
    page_title = {
        'social_settings': "Налаштування соціальних показників",
        'another': 'Інші налаштування',
    }

    breadcrumbs = {
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
        'another': {
            'name': 'Інші налаштування',
            'url': 'settings:another_settings',
        }
    }

    table_name = {
        'social_settings': 'Соціальні показники',
        'another': 'Інші налаштування'
    }

    toolbar_button = {
        'create': {
            'action': 'create',
            'url': {
                'social_settings': 'settings:create_social_settings',
                'another': 'settings:edit_social_settings',
            },
        },
        'edit': {
            'action': 'edit',
            'url': {
                'social_settings': 'settings:edit_social_settings',
                'another': '#'
            },
        },
        'view': {
            'action': 'view',
            'url': {
                'social_settings': 'settings:view_social_settings',
                'another': '#'
            },
        },
        'save': {
            'action': 'save',
            'url': {
                'social_settings': 'settings:save_social_settings',
                'another': '#'
            }, },
        'delete': {
            'action': 'delete',
            'url': {
                'social_settings': 'settings:delete_social_settings',
                'another': '#'
            }, },
        'exit': {
            'action': 'exit',
            'url': {
                'social_settings': 'settings:social_settings',
                'another': '#'
            },
        }
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        config = self.get_section_config()

        context['page_title'] = self.page_title
        context['breadcrumbs'] = self.breadcrumbs
        context['toolbar_button'] = self.toolbar_button

        return context
