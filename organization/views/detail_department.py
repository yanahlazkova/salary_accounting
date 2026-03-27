from organization.forms import UstanovaForm, DepartmentForm
from organization.models import Department
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.detail import UIDetailView


class DepartmentDetailView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDetailView):
    model = Department

    toolbar_buttons = ['exit', 'edit_department']

    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    form_class = DepartmentForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'form_title': self.get_form_title('view_department'),
        })
        return ctx