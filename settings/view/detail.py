from django.views.generic import DetailView

from settings.models import SocialSettings
from settings.view.base import SocialSettingsBaseView
from ui.buttons.base import HTMXButton

class SocialSettingsDetailView(SocialSettingsBaseView, DetailView):
    model = SocialSettings

    def get_page_buttons(self):
        obj = self.get_object()
        return [
            HTMXButton(
                label="Редагувати",
                icon="bi bi-pencil",
                url_name="social_settings:edit",
                url_kwargs={"pk": obj.pk},
            ),
            HTMXButton(
                label="Видалити",
                icon="bi bi-trash",
                url_name="social_settings:delete",
                url_kwargs={"pk": obj.pk},
                hx_method="delete",
                confirm="Видалити запис?",
            ),
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_buttons'] = self.get_page_buttons()
        return context
