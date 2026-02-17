from django.urls import reverse
from ..forms import SocialSettingsForm
from ui.forms.base import UIFormView


class SocialSettingsCreateView(UIFormView):
    template_name = "ui/base_form.html"
    form_class = SocialSettingsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["form_title"] = "Створення налаштування"
        context["form_action_url"] = reverse("social:create")
        return context
