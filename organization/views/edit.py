from organization.forms import OrganizationForm, UstanovaForm, BankAccountForm, DepartmentForm
from organization.models import Organization, Ustanova, BankAccount, Department
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


class BankAccountEditView(SettingsOrgBaseView, SectionPageToolbarMixin, UIEditView):
    model = BankAccount
    toolbar_buttons = ['exit', 'view_account']

    slug_field = 'account'
    slug_url_kwarg = 'account'

    form_class = BankAccountForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('edit_account')
        return ctx


class DepartmentEditView(SettingsOrgBaseView, SectionPageToolbarMixin, UIEditView):
    model = Department
    toolbar_buttons = ['exit', 'view_department']

    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    form_class = DepartmentForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('edit_department')
        return ctx