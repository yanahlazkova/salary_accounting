from organization.models import Ustanova
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.copy import UICopyView


class CopyUstanovaView(SettingsOrgBaseView, SectionPageToolbarMixin, UICopyView):
    model = Ustanova
    toolbar_buttons = ['exit']

    slug_field = 'kpk'
