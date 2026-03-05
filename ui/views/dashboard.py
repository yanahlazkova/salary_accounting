from django.views.generic import TemplateView

from ui.mixins.htmx import HTMXTemplateMixin
from ui.mixins.page_toolbar import SectionPageToolbarMixin


class BlockOneObject:
    def __init__(self, model_obj):
        self.model = model_obj
        self._data = None
        self._fields = None
        self._title = None
        self._toolbar_buttons: list[str] | None = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

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

    def __dict__(self):
        return {
            'title': self._title,
            # 'data': self._data,
            'fields': self._fields,
            'toolbar_buttons': self._toolbar_buttons,
        }

    def __str__(self):
        return str(self.__dict__())

    def get_fields(self, exclude_fields=None):
        if self.fields is not None:
            return self.fields

        fields_to_check = self.fields or [f.name for f in self.model._meta.fields if f.name != 'id' and f.name != 'time_created' and f.name != 'time_updated']

        return [
            self.model._meta.get_field(f).verbose_name for f in fields_to_check
        ]

class UIDashboardView(HTMXTemplateMixin, TemplateView):
    """ UI для головної сторінки розділу меню, де відображаються окремо дані однієї моделі
    та окремо дані в вигляді таблиці іншої моделі """

    # блоки контенту:
    # перший у вигляді даних одного елемента з вказаної моделі
    # другий - таблиці даних вказаної моделі (може бути інша модель)
    page_content: tuple[str] = ('ui/base_form_dashboard.html', 'base_table.html',)

    # блок сторінки з одним елементом
    # block_obj_title: dict | None = None # заголовок
    block_obj_model = None
    block_obj = None
    # obj_fields: list[str] | None = None # поля об'єкта
    # obj_data = None # дані об'єкта
    block_obj_toolbar_buttons: list[str] | None = None

    # Дані таблиці
    table_model = None
    block_table_name: str = None
    table_titles: list[str] | None = None
    table_rows: list[str] | None = None
    toolbar_buttons_table: list[str] | None = None

    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def get_obj_fields(self):
        if self.block_obj.fields is not None:
            return self.block_obj.fields

        fields_to_check = self.block_obj.fields or [f.name for f in self.block_obj_model._meta.fields if f.name != 'id' and f.name != 'time_created' and f.name != 'time_updated']

        return [
            {
                'label': self.block_obj_model._meta.get_field(f).verbose_name,
                'value': getattr(self.block_obj.data, f),
             } for f in fields_to_check
        ]

    def build_toolbar_buttons(self,button_names=None, obj=None):
        return []  # Заглушка, щоб не було помилки

    def get_table_titles(self):
        """
        Повертає заголовки таблиці
        """
        if self.table_titles is not None:
            return self.table_titles

        fields_to_check = [f.name for f in self.table_model._meta.fields]
        return [
            self.table_model._meta.get_field(f).verbose_name
            for f in fields_to_check
        ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "page_content": self.get_page_content(),
        })

        # ctx['obj'] = {
        #     'title': self.block_obj_title,
        #     'fields': self.get_obj_fields(),
        #     'toolbar_buttons': self.bild_toolbar_buttons(),
        # }
        self.block_obj = BlockOneObject(self.block_obj_model)
        # self.block_obj.buttons = self.bild_toolbar_buttons()

        ctx['table'] = {
            'name': self.block_table_name,
            "table_titles": self.get_table_titles(),
            # "toolbar_buttons": self.get_toolbar_buttons_table(),
        }

        return ctx

