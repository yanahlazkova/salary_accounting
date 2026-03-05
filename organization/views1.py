from django.apps import apps
from organization import forms
from organization.forms import OrganizationForm, UstanovaForm
from organization.models import Ustanova, Organization
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.mixins.section import AppSectionMetaMixin
from ui.views.copy import UICopyView
from ui.views.create import UICreateView
from ui.views.edit import UIEditView
from ui.views.list import UIListView


# class SettingsOrgBaseView(AppSectionMetaMixin):
#     app_label = 'organization'
#
#     slug_field = 'kpk'
#     slug_url_kwarg = 'ustanova'
#
#     form_class = OrganizationForm
#     model = Ustanova
#
#     form_title: str | None = None
#
#     def get_section_config(self):
#         if not self.app_label:
#             raise ValueError("app_label is required")
#         return apps.get_app_config(self.app_label)
#
#     def get_form_title(self, form_name):
#         if form_name == 'create' or form_name == 'main':
#             return self.get_page_subtitle(form_name)
#         else:
#             return f'{self.get_page_subtitle(form_name)} {self.kwargs[self.slug_url_kwarg]}'


# class SettingsOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIListView):
#     model = Ustanova
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#
#         data_org = Organization.objects.last()
#
#         ctx['page_content'].insert(0, 'ui/base_form_dashboard.html')
#         ctx['obj'] = {
#             'items': data_org,
#             'title': self.get_form_title('main'),
#             'fields': [f.verbose_name for f in Organization._meta.fields if f.name != 'id'],
#         }
#
#         # кнопки для організації
#         if not data_org:
#             self.toolbar_buttons = ['create_org']
#         else:
#             self.toolbar_buttons = ['edit_org']
#
#         ctx['obj'].update({
#             'buttons': self.get_toolbar_buttons()
#         })
#
#         # кнопки для таблиці
#         self.toolbar_buttons = ['exit']
#
#         ctx.update({
#             'toolbar_buttons': self.get_toolbar_buttons(),
#         })
#
#         ctx['table'].update({
#             'name': self.get_page_subtitle('table_name'),
#             'table_titles': self.get_table_titles()
#         })
#         # for c in ctx:
#         #     print(f'{c}: {ctx[c]}')
#
#         return ctx


class SettingsOrgEditView(SettingsOrgBaseView, SectionPageToolbarMixin, UIEditView):
    model = Organization

    slug_field = 'edrpou'
    slug_url_kwarg = 'edrpou'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('edit_org')
        return ctx


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


    form_class = UstanovaForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('create')
        for c in ctx:
            print(f'{c}: {ctx[c]}')
        return ctx


