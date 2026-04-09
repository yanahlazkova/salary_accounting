import time

import requests, json
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView

from pharmacy.models import Drug
from ui.mixins.htmx import HTMXTemplateMixin
from ui.mixins.section import AppSectionMetaMixin

list_pharmacy = {
    'apteka911': 'Аптека 911',
    'add': 'Аптека доброго дня',
    '1sa': 'Перша соціальна аптека',
}


class PharmacyBaseView(AppSectionMetaMixin):
    app_label = 'pharmacy'


class PharmacyBasePageView(PharmacyBaseView, HTMXTemplateMixin, TemplateView):
    page_content = ('pharmacy.html',)

    # def post(self, request, *args, **kwargs):
    #     # 1. Отримуємо текст пошуку з POST-запиту
    #     search_query = request.POST.get('search_query', '')
    #
    #     found_drugs = []
    #
    #     context = self.get_context_data()
    #     context.update({
    #         "word_search": search_query,
    #         "drugs": found_drugs,
    #     })
    #     # 3. Перевіряємо, чи це запит від HTMX
    #     if request.htmx:
    #         # Повертаємо ТІЛЬКИ шаблон таблиці
    #         return self.render_to_response(
    #             context,
    #             template="base_table.html"  # або фрагмент, що містить таблицю
    #         )
    #
    #     # Якщо це звичайний POST (наприклад, без JS), рендеримо всю сторінку
    #     return self.render_to_response(context)


    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "page_content": self.get_page_content(),
            'pharmacy': list_pharmacy,
            'form_action_url': reverse_lazy(f'{self.app_label}:search_drugs'),
        })

        return ctx


class PharmacyListDrugsView(PharmacyBaseView, HTMXTemplateMixin, ListView):
    model = Drug
    template_name = "base_table.html" # HTMX поверне тільки цей фрагмент
    htmx_template_name = 'base_table.html'
    # context_object_name = 'table' # Щоб base_table.html бачив дані як 'table'

    def post(self, request, *args, **kwargs):
        # Викликаємо метод get, щоб ListView відпрацював логіку
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        # Дістаємо query з POST (якщо форма відправлена) або з GET
        query = self.request.POST.get('search_query') or self.request.GET.get('search_query', '')
        if query:
            return self.model.objects.filter(name__icontains=query)
        return self.model.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'word_search': self.request.POST.get('search_query', ''),
            'drugs': ['drug1', 'drug2', 'drug3', 'drug4'],
        })
        return ctx
