from django.urls import reverse

from settings.models import SocialSettings
from settings.views.base import SocialSettingsBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.edit import UIEditView


class EditSocialSettings(SocialSettingsBaseView, SectionPageToolbarMixin, UIEditView):
    model = SocialSettings

    toolbar_buttons = ['exit', 'view']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('edit')
        ctx['form_action_url'] = reverse('settings:create')
        for c in ctx:
            print(f'{c}: {ctx[c]}')
        return ctx