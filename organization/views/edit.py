from organization.forms import OrganizationForm, UstanovaForm
from organization.models import Organization, Ustanova
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.edit import UIEditView


class SettingsOrgEditView(SettingsOrgBaseView, SectionPageToolbarMixin, UIEditView):
    model = Organization

    slug_field = 'edrpou'
    slug_url_kwarg = 'edrpou'

    toolbar_buttons = ['exit']

    form_class = OrganizationForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('edit_org')
        return ctx


class SettingsUstanovaEditView(SettingsOrgBaseView, SectionPageToolbarMixin, UIEditView):
    model = Ustanova
    toolbar_buttons = ['exit', 'view_ust']

    slug_field = 'kpk'
    slug_url_kwarg = 'kpk'

    form_class = UstanovaForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('edit_ust')

        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx
