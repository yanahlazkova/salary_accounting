from dataclasses import fields

from django.apps import apps
from django.shortcuts import render
from django.views import View

from organization.models import Ustanova, Organization
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.mixins.section import AppSectionMetaMixin
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
        if form_name == 'create' or form_name == 'main':
            return self.get_page_subtitle(form_name)
        else:
            return f'{self.get_page_subtitle(form_name)} {self.kwargs[self.slug_url_kwarg]}'


class SettingsOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIListView):
    # model = Organization

    toolbar_buttons = ['exit', 'edit_org']
    obj_buttons = ['edit_org']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        data_org = Organization.objects.last()

        print(f'obj_buttons: {self.obj_buttons}')

        ctx['page_content'].insert(0, 'form_view_org.html')
        ctx['org'] = {
            'items': data_org,
            'title': self.get_form_title('main'),
            'fields': [f.verbose_name for f in Organization._meta.fields if f.name != 'id'],
        }



        # розподілемо кнопки по розділам
        for url_name in self.obj_buttons:
            ctx['org'].update({
                'buttons': [button for button in ctx['toolbar_buttons'] if
                            button.url_name == f'{self.app_label}:{url_name}']
            })
            # видаляємо не потрібні для таблиці
            self.toolbar_buttons.remove(url_name)

        ctx.update({
            'toolbar_buttons': self.get_toolbar_buttons(),
        })
        for c in ctx:
            print(f'{c}: {ctx[c]}')

        return ctx


class SettingsOrgEditView(SettingsOrgView, SectionPageToolbarMixin, UIEditView):
    model = Organization
    for
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = self.get_form_title('edit_org')
        return ctx
