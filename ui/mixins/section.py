from django.apps import apps


class AppSectionMetaMixin:
    """ міксин загальних даних для розділів (додатків) """
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
            'page_title': getattr(config, 'page_title', ''),
            # 'table_name': getattr(config, 'table_name', ''),
            'icon': getattr(config, 'app_icon', None),
            # 'app_icons': getattr(config, 'app_icons', {}),
            # 'app_urls': getattr(config, 'app_urls', {}),
            # 'page_subtitle': getattr(config, 'page_subtitle', {}),
        }

        return context
