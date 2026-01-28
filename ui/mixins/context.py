class UIButtonMixin:
    toolbar_buttons = []
    # # row_buttons — шаблон кнопок
    # row_buttons = []   # ⬅ ДОДАЛИ

    def get_toolbar_buttons(self):
        return self.toolbar_buttons

    # def get_row_buttons(self, row):
    #     # get_row_buttons(row) — викликається з шаблону
    #     return self.row_buttons

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["toolbar_buttons"] = self.get_toolbar_buttons()
        # ctx["row_buttons"] = self.get_row_buttons
        return ctx
