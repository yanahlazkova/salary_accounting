from django.apps import apps

from organization.forms import OrganizationForm
from organization.models import Ustanova
from ui.mixins.section import AppSectionMetaMixin


class SettingsOrgBaseView(AppSectionMetaMixin):
    app_label = 'organization'

    slug_field = None
    slug_url_kwarg = None
    #
    # form_class = OrganizationForm
    # model = None
    #
    # form_title: str | None = None

    def get_section_config(self):
        if not self.app_label:
            raise ValueError("app_label is required")
        return apps.get_app_config(self.app_label)

    def get_form_title(self, form_name):
        if (form_name == 'create'
                or form_name == 'create_org'
                or form_name == 'create_ust'
                or form_name == 'main'
            or form_name == 'table_name'
        ):
            return self.get_page_subtitle(form_name)
        else:
            return f'{self.get_page_subtitle(form_name)} {self.kwargs[self.slug_url_kwarg]}'
