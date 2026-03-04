from organization.models import Ustanova, Organization
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import UIDashboardView


class DashboardOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDashboardView):
#     """ Загальна сторінка розділу Організація """

    block_obj_model = Organization
    table_model = Ustanova

    def get_obj_organization(self):
        self.block_obj.data = self.block_obj_model.objects.last()
        self.block_obj.title = self.get_page_subtitle('org_name')
        # buttons = ["create"] if self.block_obj.data is None else ["edit"]
        self.block_obj.toolbar_buttons = ["create_org"] if self.block_obj.data is None else ["edit_org"]
        return self.block_obj


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)


        # ctx['obj'].update({
        #     # 'data': self.get_obj_data(),
        #     'data': organization_block.data,
        #     'title': self.get_page_subtitle('org_name'),
        #     # 'buttons': self.bild_toolbar_,
        #
        # })
        ctx['obj'] = self.get_obj_organization()
        # ctx['obj'] = {
        #     'toolbar_buttons': self.build_toolbar_buttons(self.block_obj.toolbar_buttons, self.block_obj.data),
        # }

        ctx['table'].update({
            'name': self.get_page_subtitle('table_name'),
            # "toolbar_buttons": self.get_toolbar_buttons_table(),

        })

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