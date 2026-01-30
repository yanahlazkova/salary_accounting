
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView

from ui.buttons.registry import UIButtons
from ui.mixins.context import UIButtonMixin
from ui.views.base import UIListView, UIDetailView
from .models import SocialSettings
from .view.base import SocialSettingsBaseView


# icon = 'bi bi-gear me-2'
# title = 'Налаштування соціальних показників'

class SocialSettingsListView(SocialSettingsBaseView, UIButtonMixin, UIListView):
    model = SocialSettings

    queryset = SocialSettings.objects.order_by('-effective_from')

    page_blocks = [
        'social_settings.html',
        'base_table.html'
        ]

    table_name = 'Соціальні показники'

    # кнопки
    toolbar_buttons = [
        UIButtons.create(
            url_name='add_social_settings',
        )
    ]

    def get_queryset(self):
        data_db = SocialSettings.objects.all().values()

        # Створюємо список списків (ID + значення полів)
        rows_data = []
        for obj in data_db:
            rows_data.append({
                'id': obj['id'],  # Звернення через дужки (словник)
                'values': [obj.get(f.name) for f in SocialSettings._meta.fields],
                # ⬇ URL для кліку по рядку
                'row_url': reverse('view_setting', kwargs={'pk': obj['id']}),
                # кнопки
                'buttons': [
                    UIButtons.edit('edit_setting', obj['id']),
                    UIButtons.view('view_setting', obj['id']),
                ]
            })
        return rows_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        social_indicators_db = SocialSettings.objects.latest('effective_from')

        # 1. Ключові соціальні показники
        context['social_indicators'] = {
            'current_year': timezone.now().year,
            'effective_from': social_indicators_db.effective_from,
            'min_salary_monthly': f'{social_indicators_db.min_salary} грн',
            'pm_for_able_bodied': f'{social_indicators_db.pm_able_bodied} грн',
            'pdfo_rate': f'{social_indicators_db.pdfo_rate} %',
            'vz_rate': f'{social_indicators_db.vz_rate} %',  # Згідно з трудовим законодавством
            'esv_rate': f'{social_indicators_db.esv_rate} %',
        }

        return context


class SocialSettingsDetailView(SocialSettingsBaseView, UIDetailView):
    model = SocialSettings

    form_content = ['base_form_view.html']

    toolbar_buttons = [
        UIButtons.exit(url_name='settings'),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        social_indicators_db = SocialSettings.objects.get(id=self.kwargs['pk'])

        context['form_title'] = f'💰 {context['page_title']} на {social_indicators_db}'
        # 1. Ключові соціальні показники
        context['form_data'] = {
            # 'current_year': timezone.now().year,
            'effective_from': social_indicators_db.effective_from,
            'min_salary_monthly': f'{social_indicators_db.min_salary} грн',
            'pm_for_able_bodied': f'{social_indicators_db.pm_able_bodied} грн',
            'pdfo_rate': f'{social_indicators_db.pdfo_rate} %',
            'vz_rate': f'{social_indicators_db.vz_rate} %',  # Згідно з трудовим законодавством
            'esv_rate': f'{social_indicators_db.esv_rate} %',
        }

        # context['toolbar_buttons'].append(
        #     UIButtons.view('edit_social_settings')
        #     # UIButtons.edit('view_setting', self.kwargs['pk'])
        # )
        # for a in context:
        #     print(a)
        # print(f'form_data = {context['form_data']}')
        return context

    # def get_queryset(self):
    #     return SocialSettings.objects.filter(id=self.kwargs['pk']).values()

#
# class SocialSettingsCreateView(SocialSettingsBaseView, CreateView):
#     model = SocialSettings


