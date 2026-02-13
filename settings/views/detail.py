from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.detail import UIDetailView
from settings.models import SocialSettings
from settings.views.base import SocialSettingsBaseView


class SocialSettingsDetailView(SocialSettingsBaseView, SectionPageToolbarMixin, UIDetailView):
    model = SocialSettings

    page_content = ['base_form_view.html']

    toolbar_buttons = ['exit', 'edit']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        social_indicators_db = SocialSettings.objects.get(id=self.kwargs['pk'])

        # for i in context:
        #     print(f'{i}: {context[i]}')
        context['form_title'] = f'💰 {self.get_page_subtitle('view')} {social_indicators_db.effective_from}'
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

        context['toolbar_buttons'] = self.get_toolbar_buttons()

        return context

    # def get_queryset(self):
    #     return SocialSettings.objects.filter(id=self.kwargs['pk']).values()

#
# class SocialSettingsCreateView(SocialSettingsBaseView, CreateView):
#     model = SocialSettings
