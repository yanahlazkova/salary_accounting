class SectionMetaMixin:
    """ міксін для розділів (описує що повинні мати всі сторінки розділів)
    він наслідується у модулі /views/detail.py кожного додатку (розділу) """
    section_title = None
    section_icon = None
    page_titles = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = self.section_title
        context['icon_title'] = self.section_icon
        context['page_titles'] = self.page_titles,

        return context