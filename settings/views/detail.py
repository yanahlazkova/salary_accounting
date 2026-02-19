from django.urls import reverse

from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.detail import UIDetailView
from settings.models import SocialSettings
from settings.views.base import SocialSettingsBaseView


class ShowSocialSettingsView(SocialSettingsBaseView, SectionPageToolbarMixin, UIDetailView):
    model = SocialSettings

    toolbar_buttons = ['exit', 'edit', 'copy']

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['form_title'] = self.get_form_title('view')
        # for c in context:
        #     print(f'{c}: {context[c]}')

        return context



