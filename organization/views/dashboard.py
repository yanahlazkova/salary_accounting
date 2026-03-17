from django.urls import reverse

from organization.models import Ustanova, Organization
from organization.views.base import SettingsOrgBaseView
from ui.buttons.registry import UIButtons
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import UIDashboardView, BlockOneObject, BlockTable
from ui.views.helper import get_table_titles, get_obj_data


class DashboardOrgView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDashboardView):
#     """ Загальна сторінка розділу Організація """

    block_obj_model = Organization
    table_model = Ustanova

    def get_obj_organization(self):
        self.block_obj = BlockOneObject()

        self.block_obj.app_label = self.app_label

        self.block_obj.slug_field = 'edrpou'
        self.block_obj.slug_url_kwarg = 'edrpou'
        self.block_obj.title = self.get_page_subtitle('org_name')

        self.block_obj.data = self.block_obj_model.objects.last()

        obj_data = get_obj_data(self.block_obj.data) if self.block_obj.data is not None else None

        self.block_obj.fields = obj_data['fields']
        self.block_obj.toolbar_buttons = ["create_org"] if self.block_obj.data is None else ["edit_org"]

        return self.block_obj

    def get_block_ustanoty(self):
        self.block_table = BlockTable()

        self.block_table.app_label = self.app_label

        self.block_table.model = Ustanova

        self.block_table.slug_field = 'pk'
        self.block_table.slug_url_kwarg = 'pk'

        self.block_table.name = self.get_page_subtitle('table_name')
        self.block_table.table_titles = self.block_table.get_table_titles()
        self.block_table.table_rows = self.get_table_data()
        self.block_table.toolbar_buttons = ['create_ust']
        # self.block_table.toolbar_buttons = self.build_toolbar_buttons(['create_ust'], self.table_model)
        return self.block_table

    def get_table_data(self):
        slug_field = 'pk'
        slug_url_kwarg = 'pk'
        queryset = self.table_model.objects.all().values(*[
            f.name for f in Ustanova._meta.fields
                if f.name != 'id'
            ])

        rows_data = []

        for obj in queryset:
            obj['time_created'] = obj['time_created'].strftime("%d.%m.%Y %H:%M:%S")
            obj['time_updated'] = obj['time_updated'].strftime("%d.%m.%Y %H:%M:%S")
            rows_data.append({
                'values': obj,
                'row_url': reverse('organization:view_ust', kwargs={slug_url_kwarg: obj[slug_field]}), # .isoformat()}),
                'buttons': [
                    UIButtons('view_ust')
                    .set_url_name('organization:view_ust')
                    .set_kwargs({
                        slug_url_kwarg: obj[slug_field] # .isoformat()
                    }),
                ]
            })
        return rows_data

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        block_object = self.get_obj_organization()
        block_object.toolbar_buttons = block_object.get_toolbar_buttons()
        block_table = self.get_block_ustanoty()
        block_table.toolbar_buttons = block_table.get_toolbar_buttons()

        ctx.update({
            'obj': block_object,
            'table': block_table,
        })

        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx

