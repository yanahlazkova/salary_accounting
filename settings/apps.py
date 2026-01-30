from django.apps import AppConfig


class SettingsConfig(AppConfig):
    name = 'settings'
    verbose_name = 'Налаштування'

    section_icon = 'settings'
    toolbar_button = ['create', 'edit', 'view', 'save', 'delete', 'exit']
