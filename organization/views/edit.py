from organization.forms import OrganizationForm
from organization.models import Organization
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.edit import UIEditView


class SettingsOrgEditView(SettingsOrgBaseView, SectionPageToolbarMixin, UIEditView):
    model = Organization

    slug_field = 'edrpou'
    slug_url_kwarg = 'edrpou'

    form_class = OrganizationForm

    toolbar_buttons = ['exit']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('edit_org')
        return ctx