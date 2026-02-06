from django.apps import AppConfig

from ui.buttons.base import HTMXButton
from ui.buttons.registry import UIButtons
from ui.icons import ICONS


class SettingsConfig(AppConfig):
    """ загальні дані розділу Налаштування"""
    name = 'settings'
    verbose_name = 'Налаштування'

    # іконки
    app_icons = ICONS['settings']
    section_icon = app_icons['main']

    # набір кнопок
    section_buttons = {
            'social_settings': UIButtons.build(
                name="create",
                icon=ICONS['settings']['create'],
                url_name="settings:create_social_settings",
            ),
            'another': UIButtons.build(
                name="create",
                icon=ICONS['settings']['create'],
                url_name="settings:create_another_settings",
            )
        }

