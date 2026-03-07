from organization.forms import OrganizationForm
from organization.models import Organization
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.create import UICreateView


class SettingsOrgCreateView(SettingsOrgBaseView, SectionPageToolbarMixin, UICreateView):
    model = Organization

    slug_field = 'edrpou'
    slug_url_kwarg = 'edrpou'

    toolbar_buttons = ['exit']

    form_class = OrganizationForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('create_org')
        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx