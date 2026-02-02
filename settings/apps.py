from django.apps import AppConfig

from ui.buttons.icons import ICONS


class SettingsConfig(AppConfig):
    """ загальні дані розділу Налаштування"""
    name = 'settings'
    verbose_name = 'Налаштування'

    # іконка
    icons = ICONS['settings']

    # набір кнопок
    toolbar_button = ['create', 'edit', 'view', 'save', 'delete', 'exit']

    # icon = 'settings'
    #
    # actions = [
    #     {
    #         'label': 'Додати',
    #         'icon': 'plus',
    #         'url_name': 'settings:create',
    #     },
    # ]
