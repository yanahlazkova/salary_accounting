from django.urls import reverse

from organization.models import Ustanova, Organization
from organization.views.base import SettingsOrgBaseView
from ui.buttons.registry import UIButtons
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import UIDashboardView, BlockOneObject, BlockTable
from ui.views.helper import get_table_titles, get_obj_fields


class DashboardOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDashboardView):
#     """ Загальна сторінка розділу Організація """

    block_obj_model = Organization
    table_model = Ustanova

    def get_obj_organization(self):
        self.block_obj = BlockOneObject()
        self.slug_field = 'edrpou'
        self.slug_url_kwarg = 'edrpou'
        self.block_obj.title = self.get_page_subtitle('org_name')
        self.block_obj.data = self.block_obj_model.objects.last()
        self.block_obj.fields, info = get_obj_fields(self.block_obj.data) if self.block_obj.data is not None else None

        buttons = ["create_org"] if self.block_obj.data is None else ["edit_org"]
        self.block_obj.toolbar_buttons = self.build_toolbar_buttons(buttons, self.block_obj.data)

        return self.block_obj

    def get_block_ustanoty(self):
        self.block_table = BlockTable()
        self.slug_field = 'kpk'
        self.slug_url_kwarg = 'kpk'
        self.block_table.name = self.get_page_subtitle('table_name')
        self.block_table.table_titles = get_table_titles(self)
        self.block_table.table_rows = self.get_table_data()
        self.block_table.toolbar_buttons = self.build_toolbar_buttons(['create_ust'], self.table_model)
        return self.block_table

    def get_table_data(self):
        queryset = Ustanova.objects.all().values(*[
                f.name for f in Ustanova._meta.fields
                if f.name != 'id'
            ])

        rows_data = []

        for obj in queryset:
            rows_data.append({
                'values': obj,
                'row_url': reverse('organization:view_ust', kwargs={self.slug_url_kwarg: obj[self.slug_field]}), # .isoformat()}),
                'buttons': [
                    UIButtons('view_ust')
                    .set_url_name('organization:view_ust')
                    .set_kwargs({
                        self.slug_url_kwarg: obj[self.slug_field] # .isoformat()
                    }),
                ]
            })
            obj['time_created'] = obj['time_created'].strftime("%d.%m.%Y")
            obj['time_updated'] = obj['time_updated'].strftime("%d.%m.%Y")
        return rows_data


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)


        ctx.update({
            'obj': self.get_obj_organization(),
        })
        for c in ctx:
            print(f'{c}: {ctx[c]}')

        ctx['table'] = self.get_block_ustanoty()

        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx