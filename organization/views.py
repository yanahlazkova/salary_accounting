from django.apps import apps
from django.shortcuts import render
from django.views import View

from organization.models import Ustanova, Organization
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.mixins.section import AppSectionMetaMixin
from ui.views.detail import UIDetailView
from ui.views.edit import UIEditView
from ui.views.list import UIListView


class SettingsOrgBaseView(AppSectionMetaMixin):
    app_label = 'organization'

    slug_field = 'kpk'
    slug_url_kwarg = 'ustanova'

    # form_class = SettingsOrg
    model = Ustanova

    form_title: str | None = None

    def get_section_config(self):
        if not self.app_label:
            raise ValueError("app_label is required")
        return apps.get_app_config(self.app_label)

    def get_form_title(self, form_name):
        if form_name == 'create':
            return self.get_page_subtitle(form_name)
        else:
            return f'{self.get_page_subtitle(form_name)} {self.kwargs[self.slug_url_kwarg]}'





class SettingsOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIListView):
    model = Organization
    context_object_name = 'org'

    toolbar_buttons = ['edit']

    queryset = Organization.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_content'].insert(0, 'form_view_org.html')

        for c in ctx:
            print(f'{c}: {ctx[c]}')

        return ctx


class SettingsOrgEditView(SettingsOrgView, SectionPageToolbarMixin, UIEditView):
    pass