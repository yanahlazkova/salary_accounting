from organization.models import Ustanova, Organization
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import UIDashboardView


class OrganizationBlok:
    def __init__(self, org):
        self.data = org
        self.title = None
        self.buttons = ["create_org"] if org is None else ["edit_org"]


class UstanovyBlock:
    def __init__(self, queryset):
        self.queryset = queryset
        self.title = None
        self.buttons = ["create_ust"]


class DashboardOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDashboardView):
#     """ Загальна сторінка розділу Організація """

    def get_organization(self):
        return self.
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        org =
        organization_block = OrganizationBlok()
#     obj_model = Organization
#     table_model = Ustanova
#
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
#         ctx['table'].update({
#             'name': self.get_page_subtitle('table_name'),
#             "toolbar_buttons": self.get_toolbar_buttons_table(),
#
#         })
#
#         ctx['obj'].update({
#             'data': self.get_obj_data(),
#             'title': self.get_page_subtitle('main'),
#             'buttons': self.get_toolbar_buttons_own_object(),
#
#         })
#
#
#         # for c in ctx:
#         #     print(f'{c}: {ctx[c]}')
#
#         return ctx