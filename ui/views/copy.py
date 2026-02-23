from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from settings.models import SocialSettings
from ui.mixins.htmx import HTMXTemplateMixin


class UICopyView(HTMXTemplateMixin, CreateView):
    context_object_name = 'form_data'

    page_content: tuple[str] | None = ('ui/base_form.html',)
    page_subtitle: str | None = None

    toolbar_buttons: list[str] | None = None

    # Поля, які ми не хочемо копіювати
    copy_exclude_fields: list[str] = []

    # Параметри для пошуку оригіналу в URL (наприклад, 'date' або 'pk')
    copy_lookup_field: str = 'pk'
    copy_url_kwarg: str = 'pk'

    def get_initial(self):
        """ дістаємо об'єкт-джерело і перетворюємо його на початкові дані форми """
        initial = super().get_initial()

        # 1. Отримуємо значення з URL (наприклад, дату '2026-01-01')
        lookup_value = self.kwargs.get(self.copy_url_kwarg)

        if lookup_value:
            source_obj = get_object_or_404(self.model, **{self.copy_lookup_field: lookup_value}).objects.get()

            obj_data = model_to_dict(source_obj)

            # Видаляємо технічні поля (ID, pk)
            obj_data.pop('id', None)
            obj_data.pop(source_obj._meta.pk.name, None)

            for field in self.copy_exclude_fields:
                obj_data[field] = None

            initial.update(obj_data)

        return initial

    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def get_toolbar_buttons(self):
        return []  # Заглушка, щоб не було помилки

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "page_content": self.get_page_content(),
            'page_subtitle': self.page_subtitle,
            'toolbar_buttons': self.get_toolbar_buttons(),
        })
        for c in ctx:
            print(f'{c}: {ctx[c]}')

        return ctx