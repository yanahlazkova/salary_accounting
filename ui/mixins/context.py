class UIButtonMixin:

    toolbar_buttons = []

    def get_toolbar_buttons(self):
        return self.toolbar_buttons

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["toolbar_buttons"] = self.get_toolbar_buttons()
        return ctx
