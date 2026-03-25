from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from organization.forms import OrganizationForm, UstanovaForm, BankAccountForm, BankAccountCreateForm
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


class BankAccountCreateView(SettingsOrgBaseView, SectionPageToolbarMixin, UICreateView, FormView):
    model = BankAccount
    toolbar_buttons = ['exit']

    form_class = BankAccountCreateForm

    def get_initial(self):

        initial = super().get_initial()

        ustanova_kpk = self.kwargs.get('kpk')

        if ustanova_kpk:
            self.ustanova_obj = get_object_or_404(Ustanova, kpk=ustanova_kpk)
            initial['ustanova'] = self.ustanova_obj

        return initial
    #
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     return kwargs


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            'form_title': self.get_page_subtitle('create_account') + ' (' +
                          self.ustanova_obj.short_name + ')',
            'ustanova:': self.ustanova_obj.name,
        })

        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')

        return ctx


