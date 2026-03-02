from django.views.generic import TemplateView

from ui.mixins.htmx import HTMXTemplateMixin


class UIDashboardView(HTMXTemplateMixin, TemplateView):
    """ UI для головної сторінки розділу меню, де відображаються окремо дані однієї моделі
    та окремо дані в вигляді таблиці іншої моделі """

    # блоки контенту:
    # перший у вигляді даних одного елемента з вказаної моделі
    # другий - таблиці даних вказаної моделі (може бути інша модель)
    page_content: tuple[str] = ('ui/base_form_dashboard.html', 'base_table.html',)

    # блок сторінки з одним елементом
    page_subtitle: dict | None = None # заголовок
    obj_model = None
    obj_fields = None # поля об'єкта
    obj_data = None # дані об'єкта
    toolbar_buttons_own_object: list[str] | None = None

    # Дані таблиці
    table_model = None
    table_name: str = None
    table_titles: list[str] | None = None
    table_rows: list[str] | None = None
    toolbar_buttons_table: list[str] | None = None

    # набір кнопок для всіх блоків сторінки
    toolbar_buttons: list[str] | None = None

    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def get_obj_fields(self):
        if self.obj_fields is not None:
            return self.obj_fields

        fields_to_check = self.obj_fields or [f.name for f in self.obj_model._meta.fields if f.name != 'id' and f.name != 'time_created' and f.name != 'time_updated']

        return [
            self.obj_model._meta.get_field(f).verbose_name for f in fields_to_check
        ]

    def get_toolbar_buttons_own_object(self):
        if self.toolbar_buttons_own_object is not None:
            self.toolbar_buttons = self.toolbar_buttons_own_object
            return self.get_toolbar_buttons()
        return []

    def get_toolbar_buttons_table(self):
        if self.toolbar_buttons_table is not None:
            self.toolbar_buttons = self.toolbar_buttons_table
            return self.get_toolbar_buttons()
        return []

    def get_toolbar_buttons(self):
        return []  # Заглушка, щоб не було помилки

    def get_table_titles(self):
        """
        Повертає заголовки таблиці
        """
        if self.table_titles is not None:
            return self.table_titles

        fields_to_check = [f.name for f in self.table_model._meta.fields if f.name != ('time_created' or 'time_updated')]
        return [
            self.table_model._meta.get_field(f).verbose_name
            for f in fields_to_check
        ]

    # def get_table_buttons(self):
    #     self.toolbar_buttons = self.toolbar_buttons_table if self.toolbar_buttons_table is not None else []
    #     return self.get_toolbar_buttons()
    #
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "page_content": self.get_page_content(),
        })
        ctx['table'] = {
            'name': self.table_name,
            "table_titles": self.get_table_titles(),
            # "toolbar_buttons": self.get_toolbar_buttons_table(),
        }

        ctx['obj'] = {
            'title': self.page_subtitle,
            'fields': self.get_obj_fields(),
            # 'toolbar_buttons': self.get_toolbar_buttons_own_object(),
        }

        return ctx

