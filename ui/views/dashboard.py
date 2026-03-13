from django.views.generic import TemplateView

from ui.mixins.htmx import HTMXTemplateMixin


class BlockOneObject:
    def __init__(self):
        self._fields = None
        self._title = None
        self._toolbar_buttons: list[str] | None = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, name):
        self._title = name

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields):
        self._fields = fields

    @property
    def toolbar_buttons(self):
        return self._toolbar_buttons

    @toolbar_buttons.setter
    def toolbar_buttons(self, buttons):
        self._toolbar_buttons = buttons # self.build_toolbar_buttons(buttons, self._data)

    def to_dict(self):
        return {
            'title': self._title,
            # 'data': self._data,
            'fields': self._fields,
            'toolbar_buttons': self._toolbar_buttons,
        }

    def __str__(self):
        return str(self.to_dict())

class BlockTable:

    def __init__(self):
        self._table_name = None
        self._table_titles = None
        self._table_rows = None
        self._toolbar_buttons = None

    def to_dict(self):
        return {
            'name': self._table_name,
            'table_titles': self._table_titles,
            'table_rows': self._table_rows,
            'toolbar_buttons': self._toolbar_buttons,
        }

    def __str__(self):
        return str(self.to_dict())

    @property
    def table_name(self):
        return self._table_name
    @table_name.setter
    def table_name(self, name):
        self._table_name = name
    @property
    def table_titles(self):
        return self._table_titles
    @table_titles.setter
    def table_titles(self, titles):
        self._table_titles = titles
    @property
    def table_rows(self):
        return self._table_rows
    @table_rows.setter
    def table_rows(self, rows):
        self._table_rows = rows
    @property
    def toolbar_buttons(self):
        return self._toolbar_buttons
    @toolbar_buttons.setter
    def toolbar_buttons(self, buttons):
        self._toolbar_buttons = buttons


class UIDashboardView(HTMXTemplateMixin, TemplateView):
    """ UI для головної сторінки розділу меню, де відображаються окремо дані однієї моделі
    та окремо дані в вигляді таблиці іншої моделі """

    # блоки контенту:
    # перший у вигляді даних одного елемента з вказаної моделі
    # другий - таблиці даних вказаної моделі (може бути інша модель)
    page_content: tuple[str] = ('ui/base_form_dashboard.html', 'base_table.html',)

    # блок сторінки з одним елементом
    block_obj_model = None
    block_obj = None

    # Дані таблиці
    table_model = None
    block_table = None

    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def build_toolbar_buttons(self,button_names=None, obj=None):
        return []  # Заглушка, щоб не було помилки

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "page_content": self.get_page_content(),
        })


        return ctx

