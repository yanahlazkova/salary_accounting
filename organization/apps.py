from django.apps import AppConfig

from ui.icons import ICONS


class OrganizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organization'

    verbose_name = 'Дані організації'

    page_title = "Налаштування даних організації"

    # іконки
    app_icons = ICONS['settings']
    app_icon = app_icons['main']

    page_subtitle = {
        'main': 'Данні організації',
        'table_name': 'Установи організації',
        'create': 'Створення установи',
        'create_org': 'Введення даних організації',
        'edit': 'Редагування установи',
        'edit_org': 'Редагування даних організації',
        'view': 'Перегляд установи ',
        'copy': 'Копіювання даних установи від ',
    }

    app_urls = {
        'exit': 'settings',
        'create': 'create',
        'create_org': 'create_org',
        'edit': 'edit',
        'edit_org': 'edit_org',
        'view': 'view',
        'copy': 'copy',
    }


