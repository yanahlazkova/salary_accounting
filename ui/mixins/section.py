from django.apps import apps

class AppSectionMixin:
    app_label = None

    def get_section_config(self):
        if not self.app_label:
            raise ValueError("app_label is required")
        return apps.get_app_config(self.app_label)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = self.get_section_config()

        context['section'] = {
            'title': config.verbose_name,
            'section_icon': getattr(config, 'section_icon', None),
            'icons': getattr(config, 'app_icons', []),
            'actions': getattr(config, 'section_buttons', []),
        }

        return context
