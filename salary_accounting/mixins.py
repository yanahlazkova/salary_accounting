class SectionMetaMixin:
    page_title = None
    page_icon = None
    button_icons = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_icon'] = self.page_icon
        context['button_icons'] = self.button_icons
        return context
