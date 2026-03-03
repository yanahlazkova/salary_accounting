from django.urls import reverse
from django.utils import timezone
from settings.models import SocialSettings
from settings.views.base import SocialSettingsBaseView
from ui.buttons.registry import UIButtons
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.list import UIListView


class SocialSettingsListView(SocialSettingsBaseView,
                             SectionPageToolbarMixin,
                             UIListView):
    # model = SocialSettings

    toolbar_buttons = ['create']

    def get_queryset(self):
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
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        social_indicators_db = (
            SocialSettings.objects
            .filter(effective_from__lte=today)
            .order_by('-effective_from')
            .first()
        )
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
        context['table'].update({
            'name': self.get_page_subtitle('main'),
        })
        # for ctx in context:
        #     print(f'{ctx}: {context[ctx]}')

        return context
