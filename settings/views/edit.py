from django.urls import reverse, reverse_lazy

from settings.forms import SocialSettingsForm
from settings.models import SocialSettings
from settings.views.base import SocialSettingsBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.edit import UIEditView


class EditSocialSettingsView(SocialSettingsBaseView, SectionPageToolbarMixin, UIEditView):
    model = SocialSettings
    form_class = SocialSettingsForm

    # Куди редиректити після успішного збереження
    success_url = reverse_lazy('settings:social_settings')

    toolbar_buttons = ['exit', 'view']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('edit')
        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx