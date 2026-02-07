from django.views.generic import ListView
from .base import SocialSettingsBaseView
from ..models import SocialSettings

class SocialSettingsListView(SocialSettingsBaseView, ListView):
    model = SocialSettings
    # template_name = 'social_settings/list.html'
    # page_subtitle = 'Соціальні показники'

    page_blocks = [
        'social_settings.html',
        'base_table.html'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_blocks'] = self.page_blocks
        return context
