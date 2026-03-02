from organization.models import Ustanova, Organization
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import UIDashboardView


class DashboardOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDashboardView):
    """ Загальна сторінка розділу Організація """
    obj_model = Organization
    table_model = Ustanova

    def get_obj_data(self):
        return self.obj_model.objects.last()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # ctx['obj'].update({
        #     'fields': self.get_obj_data(),
        # })
        for c in ctx:
            print(f'{c}: {ctx[c]}')

        return ctx