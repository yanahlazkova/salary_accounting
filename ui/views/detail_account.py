from organization.forms import UstanovaForm, BankAccountForm
from organization.models import BankAccount
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.detail import UIDetailView


class BankAccountDetailView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDetailView):
    model = BankAccount

    toolbar_buttons = ['exit', 'edit_account']

    slug_field = 'account'
    slug_url_kwarg = 'account'

    form_class = BankAccountForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'form_title': self.get_form_title('view_account'),
        })
        return ctx