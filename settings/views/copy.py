from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from settings.forms import SocialSettingsForm
from settings.models import SocialSettings
from settings.views.base import SocialSettingsBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.copy import UICopyView


class CopySocialSettingsView(SocialSettingsBaseView, SectionPageToolbarMixin, UICopyView):

    toolbar_buttons = ['exit']
    copy_exclude_fields = ['effective_from', 'min_salary', 'pm_able_bodied']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'form_title': self.get_form_title('copy'),
        })

        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')

        return ctx