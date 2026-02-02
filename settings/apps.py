from django.apps import AppConfig

from ui.buttons.base import HTMXButton
from ui.icons import ICONS


class SettingsConfig(AppConfig):
    """ загальні дані розділу Налаштування"""
    name = 'settings'
    verbose_name = 'Налаштування'

    # іконки
    app_icons = ICONS['settings']
    section_icon = app_icons['main']

    # набір кнопок
    section_buttons = [
        HTMXButton(
            label="Додати",
            icon=ICONS['settings']['create'],
            url_name="settings:create_social_settings",
        )
    ]

    toolbar_button = ['create', 'edit', 'view', 'save', 'delete', 'exit']
