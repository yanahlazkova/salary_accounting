from organization.models import Ustanova, Organization
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import UIDashboardView


class DashboardOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDashboardView):
#     """ Загальна сторінка розділу Організація """

    block_obj_model = Organization
    table_model = Ustanova

    def get_obj_organization(self):
        self.slug_field = 'edrpou'
        self.slug_url_kwarg = 'edrpou'
        self.block_obj.data = self.block_obj_model.objects.last()
        self.block_obj.fields = self.get_obj_fields() if self.block_obj.data is not None else None
        self.block_obj.title = self.get_page_subtitle('org_name')
        buttons = ["create_org"] if self.block_obj.data is None else ["edit_org"]
        self.block_obj.toolbar_buttons = self.build_toolbar_buttons(buttons, self.block_obj.data)
        return self.block_obj

    def get_table_ustanoty(self):
        self.slug_field = 'kpk'
        self.slug_url_kwarg = 'kpk'
        self.block_table.table_name = self.get_page_subtitle('table_name')
        self.block_table.table_titles = self.get_table_titles()
        self.block_table.table_rows = self.table_model.objects.all().values()
        self.block_table.toolbar_buttons = self.build_toolbar_buttons(['create_ust'], self.table_model)
        return self.block_table


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['obj'] = self.get_obj_organization()

        ctx['table'] = self.get_table_ustanoty()



        # ctx['table'].update({
        #     'name': self.get_page_subtitle('table_name'),
        #     # "toolbar_buttons": self.get_toolbar_buttons_table(),
        #
        # })

#     toolbar_buttons_own_object = None
#     toolbar_buttons_table = ['create']
#
#     def get_obj_data(self):
#         obj_data = self.obj_model.objects.last()
#         if obj_data is None:
#             self.toolbar_buttons_own_object = ['create_org']
#         else:
#             self.toolbar_buttons_own_object = ['edit_org']
#         return obj_data
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#
#         data = self.get_obj_data()
#         print(f'data: {data}')
#
#         self.toolbar_buttons_own_object =['create_org' if self.get_obj_data() is None else ['edit_org']]
#

#
#
#
#
        for c in ctx:
            print(f'{c}: {ctx[c]}')
#
        return ctx