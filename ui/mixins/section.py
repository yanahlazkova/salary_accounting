from django.apps import apps

class AppSectionMixin:
    app_label = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.app_label:
            raise ValueError("app_label is required")

        config = apps.get_app_config(self.app_label)

        context['section_title'] = config.verbose_name
        context['section_icon'] = getattr(config, 'section_icon', None)

        return context
