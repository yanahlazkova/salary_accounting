
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from ui.buttons.registry import UIButtons
from ui.mixins.context import UIButtonMixin
from ui.views.base import UIListView
from .models import SocialSettings


icon = 'bi bi-gear me-2'
title = 'Налаштування соціальних показників'

class SocialSettingsListView(UIButtonMixin, UIListView):
    model = SocialSettings
    template_name = "base_page.html"
    htmx_template_name = "base_content.html"
    page_icon = icon
    page_title = title
    page_blocks = [
        'social_settings.html',
        'base_table.html'
        ]

    # кнопки
    toolbar_buttons = [
        UIButtons.create(
            url_name='add_social_settings',
            app_icon='setting'
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
                'row_url': reverse('view', kwargs={'pk': obj['id']}),
                # кнопки
                'buttons': [
                    UIButtons.edit('edit', obj['id']),
                    UIButtons.view('view', obj['id']),
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

