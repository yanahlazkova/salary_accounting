from django.http import HttpResponse

from ui.views.base import UIListView
from .models import SocialSettings


icon = 'bi bi-gear me-2'
title = 'Налаштування соціальних показників'

class SocialSettingsListView(UIListView):
    model = SocialSettings
    # context_object_name = 'social_indicators'
    template_name = "base_page.html"
    htmx_template_name = "base_content.html"
    page_icon = icon
    page_title = title
    page_blocks = [
        'social_settings.html',
        'base_table.html'
        ]


