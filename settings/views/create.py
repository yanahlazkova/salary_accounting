from django.urls import reverse

from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.create import UICreateView
from .base import SocialSettingsBaseView
from ..forms import SocialSettingsForm
from ..models import SocialSettings


class CreateSocialSettingsView(SocialSettingsBaseView, SectionPageToolbarMixin,UICreateView):
    toolbar_buttons = ['exit']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'form_title': self.get_form_title('create'),
        })
        return ctx
