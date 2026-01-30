from ui.buttons.icons import ICONS
from ui.mixins.section import AppSectionMixin


# class SocialSettingsBaseView(SectionMetaMixin, AppSectionMeta):
class SocialSettingsBaseView(AppSectionMixin):
    app_label = 'settings'

    page_title = "Соціальні показники"
    page_icon = ICONS['settings']['main']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = self.page_title
        context['page_icon'] = self.page_icon
        context['toolbar_buttons'] = self.toolbar_buttons

        return context

