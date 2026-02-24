from django.apps import AppConfig

from ui.icons import ICONS


class UstanovaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ustanova'

    verbose_name = 'Дані установи'

    page_title = "Встановлення даних установи"

    # іконки
    app_icons = ICONS['settings']
    app_icon = app_icons['main']

    page_subtitle = {
        'main': 'Соціальні показники',
        'create': 'Створення соціальних показників',
        'edit': 'Редагування соціальних показників за',
        'view': 'Соціальні показники на',
        'copy': 'Створення соціальних показників',
    }

    app_urls = {
        'exit': 'social_settings',
        'create': 'create',
        'edit': 'edit',
        'view': 'view',
        'copy': 'copy',
    }


