from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.detail import UIDetailView
from settings.models import SocialSettings
from settings.views.base import SocialSettingsBaseView


class ShowSocialSettings(SocialSettingsBaseView, SectionPageToolbarMixin, UIDetailView):
    model = SocialSettings

    # slug_url_kwarg = 'pk'
    slug_field = 'effective_from'
    slug_url_kwarg = 'slug_setting'

    page_content = ['base_form_view.html']

    toolbar_buttons = ['exit', 'edit']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['page_subtitle'] = self.get_page_subtitle('view')
        context['form_title'] = f'💰 {self.get_page_subtitle('view')} {context['object']}'

        return context


class EditSocialSettings(SocialSettingsBaseView, SectionPageToolbarMixin, UIDetailView):
    model = SocialSettings
    slug_field = 'effective_from'
    slug_url_kwarg = 'slug_setting'
    page_content = ['base_form.html']
    toolbar_buttons = ['exit', 'view']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = f'{self.get_page_subtitle('edit')} {ctx['object']}'
        for c in ctx:
            print(f'{c}: {ctx[c]}')
        return ctx


