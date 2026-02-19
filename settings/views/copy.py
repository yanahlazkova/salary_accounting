from django.views.generic import CreateView

from settings.forms import SocialSettingsForm
from settings.models import SocialSettings
from ui.views.copy import UICopyView


class CopySocialSettingsView(UICopyView):
    model = SocialSettings
    form_class = SocialSettingsForm