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
        'org_name': 'Данні організації',
        'table_name': 'Установи організації',
        'table_accounts': 'Банківські рахунки',
        'create_ust': 'Створення установи',
        'create_org': 'Введення даних організації',
        'edit_ust': 'Редагування установи',
        'edit_org': 'Редагування даних організації',
        'view_ust': 'Перегляд установи КПК ',
        'copy_ust': 'Копіювання даних установи від ',
        'view_account': 'Перегляд банківського рахунку',
        'create_account': 'Створення банківського рахунку',
        'edit_account': 'Редагування банківського рахунку',
    }

    app_urls = {
        'exit': 'settings',
        'create_org': 'create_org',
        'edit_org': 'edit_org',
        'create_ust': 'create_ust',
        'edit_ust': 'edit_ust',
        'view_ust': 'view_ust',
        'copy_ust': 'copy_ust',
        'create_account': 'create_account',
        'view_account': 'view_account',
    }


