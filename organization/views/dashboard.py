from organization.models import Ustanova, Organization
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import UIDashboardView


class DashboardOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDashboardView):
    """ Загальна сторінка розділу Організація """
    obj_model = Organization
    table_model = Ustanova

    toolbar_buttons_own_object = []
    toolbar_buttons_table = ['create']

    def get_obj_data(self):
        return self.obj_model.objects.last()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        self.toolbar_buttons_own_object.append('create_org' if self.get_obj_data() is None else ['exit'])

        ctx['table'].update({
            'name': self.get_page_subtitle('table_name'),
            "toolbar_buttons": self.get_toolbar_buttons_table(),

        })

        ctx['obj'].update({
            'title': self.get_page_subtitle('main'),
            'buttons': self.get_toolbar_buttons_own_object(),

        })
        for c in ctx:
            print(f'{c}: {ctx[c]}')

        return ctx