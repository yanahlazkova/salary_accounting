from django.apps import AppConfig
from ui.icons import ICONS


class SettingsConfig(AppConfig):
    """ загальні дані розділу Кадри"""
    name = 'settings'
    verbose_name = 'Налаштування'

    page_title = "Налаштування соціальних показників"
    # table_name = 'Соціальні показники'

    # іконки
    app_icons = ICONS['settings']
    app_icon = app_icons['main']

    page_subtitle = {
        'main': 'Соціальні показники',
        'create': 'Додавання нових налаштувань',
        'edit': 'Редагування налаштувань за ',
        'view': 'Перегляд налаштувань за ',
    }


    app_urls = {
        'exit': 'social_settings',
        'create': 'create',
        'edit': 'edit',
        'view': 'view',
    }
