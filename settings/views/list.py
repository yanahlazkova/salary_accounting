from django.urls import reverse
from django.utils import timezone
from ui.buttons.registry import UIButtons

from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.list import UIListView
from .base import SocialSettingsBaseView
from ..models import SocialSettings

class SocialSettingsListView(SocialSettingsBaseView, SectionPageToolbarMixin, UIListView):
    model = SocialSettings

    toolbar_buttons = ['create', 'exit']


    def get_queryset(self):
        data_db = SocialSettings.objects.order_by('-effective_from')

        # Створюємо список списків (ID + значення полів)
        rows_data = []
        for obj in data_db:
            rows_data.append({
                'id': obj.id,
                'values': [
                    obj.id,
                    obj.effective_from.strftime("%d.%m.%Y"),
                    obj.min_salary,
                    obj.pm_able_bodied,
                    obj.pdfo_rate,
                    obj.vz_rate,
                    obj.esv_rate,
                    obj.time_created.strftime("%d.%m.%Y"),
                    obj.time_updated.strftime("%d.%m.%Y"),
                ],
                # ⬇ URL для кліку по рядку
                # 'row_url': reverse('settings:view', kwargs={'date': obj['effective_from']}),
                'row_url': reverse('settings:view', kwargs={self.slug_url_kwarg: getattr(obj, self.slug_field).isoformat()}),
                # кнопки
                'buttons': [
                    # UIButtons('view').set_url_name('settings:view').set_kwargs({'date': obj['effective_from']}),
                    UIButtons('view')
                    .set_url_name('settings:view')
                    .set_kwargs({
                        self.slug_url_kwarg: getattr(obj, self.slug_field).isoformat()
                    }),
                ]
            })
            # print(f'**: {self.slug_url_kwarg}: {obj[self.slug_field]}')
        return rows_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        social_indicators_db = (
            SocialSettings.objects
            .filter(effective_from__lte=today)
            .order_by('-effective_from')
            .first()
        )
        # social_indicators_db = self.queryset.latest('effective_from')
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
        # контент складається з двох блоків. Додамо до загального блоку ще один
        context['page_content'].insert(0, 'social_settings.html')
        context['table_name'] = self.get_page_subtitle('main')
        # for ctx in context:
        #     print(f'{ctx}: {context[ctx]}')
        return context
