from django.shortcuts import get_object_or_404

from organization.forms import OrganizationForm, UstanovaForm, BankAccountForm
from organization.models import Organization, Ustanova, BankAccount
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


class SettingsUstanovaCreateView(SettingsOrgBaseView, SectionPageToolbarMixin, UICreateView):
    model = Ustanova
    toolbar_buttons = ['exit']

    slug_field = 'kpk'
    slug_url_kwarg = 'kpk'

    form_class = UstanovaForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('create_ust')
        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx


class BankAccountCreateView(SettingsOrgBaseView, SectionPageToolbarMixin, UICreateView):
    model = BankAccount
    toolbar_buttons = ['exit']

    # slug_field = 'kpk'
    # slug_url_kwarg = 'kpk'

    form_class = BankAccountForm

    def get_initial(self):

        initial = super().get_initial()

        ustanova_kpk = self.kwargs.get('ustanova_kpk')

        if ustanova_kpk:
            ustanova = get_object_or_404(Ustanova, kpk=ustanova_kpk)
            initial['ustanova'] = ustanova.kpk

        return initial


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ustanova_kpk = self.kwargs.get('ustanova_kpk')

        ctx.update({
            'form_title': self.get_form_title('create_account'),
            # 'ustanova':
        })

        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')

        return ctx


