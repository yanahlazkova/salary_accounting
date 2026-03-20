from organization.forms import UstanovaForm
from organization.models import Ustanova, BankAccount
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import BlockTable
from ui.views.detail import UIDetailView
from ui.views.helper import get_table_data


class SettingsUstanovaDetailView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDetailView):
    model = Ustanova
    toolbar_buttons = ['exit', 'edit_ust']

    accounts_block = BlockTable()

    slug_field = 'kpk'
    slug_url_kwarg = 'kpk'

    form_class = UstanovaForm

    def get_accounts_block(self):
        accounts_block = BlockTable()
        self.accounts_block.app_label = self.app_label

        self.accounts_block.model = BankAccount

        self.accounts_block.slug_field = 'account'
        self.accounts_block.slug_url_kwarg = 'account'
        accounts = BankAccount.objects.filter(account=self.accounts_block.slug_url_kwarg)

        self.accounts_block.name = self.get_page_subtitle('table_accounts')
        self.accounts_block.table_titles = self.accounts_block.get_table_titles()
        self.accounts_block.table_rows = get_table_data(self, revers_url='organization:view_account', queryset=accounts)
        self.accounts_block.toolbar_buttons = ['create_account']
        self.accounts_block.toolbar_buttons = self.accounts_block.get_toolbar_buttons()

        return self.accounts_block


    def get_departments_block(self):
        pass

    def change_page_content(self):
        page_content = self.get_page_content()
        page_content[0] = 'ustanova_view.html'
        page_content.append('base_table.html')

        return page_content

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'form_title': self.get_form_title('view_ust'),
            'page_content': self.change_page_content(),
            'accounts': self.get_accounts_block(),
        })
        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx
