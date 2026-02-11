from django.urls import reverse
from django.utils import timezone
from ui.buttons.registry import UIButtons

from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.list import UIListView
from .base import SocialSettingsBaseView
from ..models import SocialSettings

class SocialSettingsListView(SocialSettingsBaseView, SectionPageToolbarMixin, UIListView):
    model = SocialSettings

    queryset = SocialSettings.objects.order_by('-effective_from')

    page_blocks = [
        'social_settings.html',
        'base_table.html'
    ]

    page_actions = [
        {
            'action': 'create',
            'url': 'settings:create_social_settings',
        },
    #     {'action': 'edit', 'url': 'settings:create_social_settings'},
    #     {'action': 'views', 'url': 'settings:edit_social_settings'},
    #     {'action': 'save', 'url': 'settings:view_social_settings'},
    #     {'action': 'delete', 'url': 'settings:save_social_settings'},
        {'action': 'exit', 'url': 'settings:create_social_settings'}
    ]
    # table_name = 'Соціальні показники'
    actions = ['create', 'exit']

    def get_queryset(self):
        data_db = SocialSettings.objects.all().values()

        # Створюємо список списків (ID + значення полів)
        rows_data = []
        for obj in data_db:
            rows_data.append({
                'id': obj['id'],  # Звернення через дужки (словник)
                'values': [obj.get(f.name) for f in SocialSettings._meta.fields],
                # 'values': [obj.get(f) for f in self.table_titles],
                # ⬇ URL для кліку по рядку
                'row_url': reverse('settings:view_social_settings', kwargs={'pk': obj['id']}),
                # кнопки
                'buttons': [
                    UIButtons('view').set_url_name('settings:view_social_settings').set_pk(obj['id']),
                ]
            })
        return rows_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print('context:', context)

        social_indicators_db = self.queryset.latest('effective_from')
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

        # if context['toolbar_buttons']:
        #     for button in context['toolbar_buttons']:
        #         button.icon = context['section']['set_icons'][button.name]

        # context['table_name'] = self.get_page('main')['name']

        return context
