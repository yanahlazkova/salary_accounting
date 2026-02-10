from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView

from ui.buttons.registry import UIButtons
from ui.views.detail import UIDetailView
from ui.views.list import UIListView
from .models import SocialSettings
from .views.base import SocialSettingsBaseView
from .views.list import SocialSettingsListView


# class SocialSettingsList(SocialSettingsListView, UIListView):
#     model = SocialSettings
#
#
#     queryset = SocialSettings.objects.order_by('-effective_from')
#
#     def get_queryset(self):
#         data_db = SocialSettings.objects.all().values()
#
#         # Створюємо список списків (ID + значення полів)
#         rows_data = []
#         for obj in data_db:
#             rows_data.append({
#                 'id': obj['id'],  # Звернення через дужки (словник)
#                 'values': [obj.get(f.name) for f in SocialSettings._meta.fields],
#                 # ⬇ URL для кліку по рядку
#                 'row_url': reverse('settings:view_social_settings', kwargs={'pk': obj['id']}),
#                 # кнопки
#                 'buttons': [
#                     UIButtons.view('settings:view_social_settings', obj['id']),
#                 ]
#             })
#         return rows_data
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         social_indicators_db = self.queryset.latest('effective_from')
#
#         # context['breadcrumbs'] = [
#         #     {
#         #         'name': context['all_page']['home']['name'],
#         #         'url': context['all_page']['home']['url'],
#         #     },
#         #     {
#         #         'name': context['all_page']['social_settings']['name'],
#         #         'url': context['all_page']['social_settings']['url'],
#         #     }
#         # ]
#
#         # 1. Ключові соціальні показники
#         context['social_indicators'] = {
#             'current_year': timezone.now().year,
#             'effective_from': social_indicators_db.effective_from,
#             'min_salary_monthly': f'{social_indicators_db.min_salary} грн',
#             'pm_for_able_bodied': f'{social_indicators_db.pm_able_bodied} грн',
#             'pdfo_rate': f'{social_indicators_db.pdfo_rate} %',
#             'vz_rate': f'{social_indicators_db.vz_rate} %',  # Згідно з трудовим законодавством
#             'esv_rate': f'{social_indicators_db.esv_rate} %',
#         }
#
#         for i in context:
#             print(f'{i}: {context[i]}')
#
#         return context


class SocialSettingsDetailView(SocialSettingsBaseView, UIDetailView):
    model = SocialSettings

    form_content = ['base_form_view.html']

    toolbar_buttons = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # icons = context['section']['icons']
        # buttons_name = context['section']['toolbar_buttons']

        # створити функцію яка повертає набір кнопок
        # context['toolbar_buttons'] = get_buttons(buttons_name, self.kwargs['pk'], icons)

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

        for i in context:
            print(f'{i}: {context[i]}')

        return context

    # def get_queryset(self):
    #     return SocialSettings.objects.filter(id=self.kwargs['pk']).values()

#
# class SocialSettingsCreateView(SocialSettingsBaseView, CreateView):
#     model = SocialSettings
