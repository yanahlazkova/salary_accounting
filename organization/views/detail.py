from organization.forms import UstanovaForm
from organization.models import Ustanova
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.detail import UIDetailView


class SettingsUstanovaDetailView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDetailView):
    model = Ustanova
    toolbar_buttons = ['exit', 'edit_ust']

    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    form_class = UstanovaForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('view_ust')
        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx
