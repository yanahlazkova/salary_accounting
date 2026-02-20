from django.urls import reverse

from ui.views.create import UICreateView
from ..forms import SocialSettingsForm
from ..models import SocialSettings


class CreateSocialSettingsView(UICreateView):
    # template_name = "ui/base_form.html"
    model = SocialSettings
    form_class = SocialSettingsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["form_title"] = "Створення налаштування"
        context["form_action_url"] = reverse("social:create")
        return context
