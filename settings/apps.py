from django.apps import AppConfig

from ui.buttons.base import HTMXButton
from ui.buttons.registry import UIButtons
from ui.icons import ICONS


class SettingsConfig(AppConfig):
    """ загальні дані розділу Кадри"""
    name = 'settings'
    verbose_name = 'Налаштування'

    # іконки
    app_icons = ICONS['settings']
    app_icon = app_icons['main']


