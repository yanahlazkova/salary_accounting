from django.apps import AppConfig
from ui.icons import ICONS


class SettingsConfig(AppConfig):
    """ загальні дані розділу Кадри"""
    name = 'settings'
    verbose_name = 'Налаштування'

    page_title = "Налаштування соціальних показників"
    table_name = 'Соціальні показники'

    # іконки
    app_icons = ICONS['settings']
    app_icon = app_icons['main']

    actions = {
        'main': {
            'name': 'Соціальні показники',
            'url': 'social_settings',
        },
        'create': {
            'name': 'Додавання нових налаштувань',
            'url': 'create_social_settings',
        },
        'edit': {
            'name': 'Редагування налаштувань за ',
            'url': 'edit_social_settings',
        },
        'view': {
            'name': 'Перегляд налаштувань за ',
            'url': 'view_social_settings',
        },
        'exit': {
            'url': 'social_settings',
        },
    }

