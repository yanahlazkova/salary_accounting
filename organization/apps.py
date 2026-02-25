from django.apps import AppConfig

from ui.icons import ICONS


class OrganizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organization'

    verbose_name = 'Дані організації'

    page_title = "Встановлення даних організації"

    # іконки
    app_icons = ICONS['settings']
    app_icon = app_icons['main']

    page_subtitle = {
        'main': 'Налаштування даних організації',
        'create': 'Створення установи',
        'edit': 'Редагування установи',
        'edit_org': 'Редагування даних організації',
        'view': 'Перегляд установи ',
        'copy': 'Копіювання даних установи від ',
    }

    app_urls = {
        'exit': 'settings',
        'create': 'create',
        'edit': 'edit',
        'edit_org': 'edit_org',
        'view': 'view',
        'copy': 'copy',
    }


