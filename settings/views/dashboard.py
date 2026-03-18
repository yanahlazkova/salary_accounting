from django.urls import reverse
from django.utils import timezone
from settings.models import SocialSettings
from settings.views.base import SocialSettingsBaseView
from ui.buttons.registry import UIButtons
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import UIDashboardView, BlockOneObject, BlockTable
from ui.views.helper import get_obj_data


class DashboardSettingsView(SocialSettingsBaseView,SectionPageToolbarMixin, UIDashboardView):
    def get_social_settings(self):
        # self.block_obj = BlockOneObject()
        #
        # self.block_obj.app_label = self.app_label
        #
        # self.block_obj.slug_field = 'effective_from'
        # self.block_obj.slug_url_kwarg = 'effective_from'
        #
        # self.block_obj.title = self.get_form_title('main')
        #
        # today = timezone.now().date()
        # self.block_obj.data = (
        #     SocialSettings.objects
        #     .filter(effective_from__lte=today) # Діє з <= поточної дати
        #     .order_by('-effective_from')
        #     .first()
        # )
        #
        # obj_data = get_obj_data(self.block_obj.data) if self.block_obj.data is not None else None
        # i = 0
        # left = []
        # right = []
        # for key, field in obj_data['fields'].items():
        #     i += 1
        #     left.append({key: field}) if i <= 3 else right.append({key: field})
        #
        # obj_data['fields'] = {
        #     'left': left,
        #     'right': right,
        # }
        # print(f'fields: {obj_data['fields']}')
        #
        # self.block_obj.fields = obj_data['fields']
        # # self.block_obj.toolbar_buttons = ["create"] if self.block_obj.data is None else ["edit_org"]

        today = timezone.now().date()

        social_indicators_db = (
            SocialSettings.objects
            .filter(effective_from__lte=today)  # Діє з <= поточної дати
            .order_by('-effective_from')
            .first()
        )
        self.block_obj = {
            'current_year': timezone.now().year,
            'effective_from': social_indicators_db.effective_from,
            'min_salary_monthly': f'{social_indicators_db.min_salary} грн',
            'pm_for_able_bodied': f'{social_indicators_db.pm_able_bodied} грн',
            'pdfo_rate': f'{social_indicators_db.pdfo_rate} %',
            'vz_rate': f'{social_indicators_db.vz_rate} %',  # Згідно з трудовим законодавством
            'esv_rate': f'{social_indicators_db.esv_rate} %',
        }
        return self.block_obj

    def get_block_table_social_settings(self):
        self.block_table = BlockTable()

        self.block_table.app_label = self.app_label

        self.block_table.model = SocialSettings

        self.block_table.slug_field = 'effective_from'
        self.block_table.slug_url_kwarg = 'effective_from'

        self.block_table.name = self.get_page_subtitle('table_name')
        self.block_table.table_titles = self.block_table.get_table_titles()
        self.block_table.table_rows = self.get_table_data()
        self.block_table.toolbar_buttons = ['create']
        self.block_table.toolbar_buttons = self.block_table.get_toolbar_buttons()

        return self.block_table

    def get_table_data(self):
        queryset = (
            SocialSettings.objects
            .order_by('-effective_from')
            .values(*[
                f.name for f in SocialSettings._meta.fields
                if f.name != 'id'
            ])
        )
        rows_data = []

        for obj in queryset:
            rows_data.append({
                'values': obj,
                'row_url': reverse('settings:view', kwargs={self.slug_url_kwarg: obj[self.slug_field].isoformat()}),
                'buttons': [
                    UIButtons('view')
                    .set_url_name('settings:view')
                    .set_kwargs({
                        self.slug_url_kwarg: obj[self.slug_field].isoformat()
                    }),
                ]
            })
            obj['effective_from'] = obj['effective_from'].strftime("%d.%m.%Y")
            obj['time_created'] = obj['time_created'].strftime("%d.%m.%Y")
            obj['time_updated'] = obj['time_updated'].strftime("%d.%m.%Y")

        return rows_data

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['page_content'].pop(0)
        ctx['page_content'].insert(0, 'social_settings.html')

        print(f'{ctx['page_content']}')

        ctx.update({
            'social_indicators': self.get_social_settings(),
            'table': self.get_block_table_social_settings(),
        })

        return ctx