from organization.forms import UstanovaForm
from organization.models import Ustanova
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.detail import UIDetailView


class SettingsUstanovaDetailView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDetailView):
    model = Ustanova
    toolbar_buttons = ['exit', 'edit_ust']

    slug_field = 'kpk'
    slug_url_kwarg = 'kpk'

    form_class = UstanovaForm

    def change_page_content(self):
        page_content = self.get_page_content()
        page_content[0] = 'base_table.html'

        return page_content

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'form_title': self.get_form_title('view_ust'),
            'page_content': self.change_page_content(),
        })
        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx
