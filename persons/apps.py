from django.apps import AppConfig

from ui.buttons.registry import UIButtons
from ui.icons import ICONS


class PersonsConfig(AppConfig):
    """ загальні дані розділу Налаштування"""
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'persons'
    verbose_name = 'Кадри'

    # іконки
    app_icons = ICONS['persons']
    app_icon = app_icons['main']

    # # набір кнопок
    section_buttons = {
        'social_settings': UIButtons('create').build()
        # 'social_settings': UIButtons.build(
            # name="create",
            # icon=ICONS['persons']['create'],
            # url_name="persons:add_persons",
        # ),
    }