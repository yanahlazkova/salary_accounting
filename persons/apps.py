from django.apps import AppConfig

from ui.icons import ICONS


class PersonsConfig(AppConfig):
    """ загальні дані розділу Налаштування"""
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'persons'
    verbose_name = 'Кадри'

    # набір іконок
    section_icons = ICONS['persons']

    # набір кнопок
    toolbar_button = ['create', 'edit', 'view', 'save', 'delete', 'exit']
