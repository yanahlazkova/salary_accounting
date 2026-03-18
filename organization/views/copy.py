from organization.models import Ustanova
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.copy import UICopyView


class CopySubgroupUstanovaView(SettingsOrgBaseView, SectionPageToolbarMixin, UICopyView):
    """ копіювання підгруппи установи """
    model = Ustanova
    toolbar_buttons = ['exit']

    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'form_title': self.get_form_title('copy'),
        })

        return ctx
