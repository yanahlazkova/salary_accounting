import time
import requests, json
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView
from django.utils import timezone

from pharmacy.helper_pharmacy import get_categories_whith_page_cite_apteka911, \
    update_category, get_categories_with_sitemap
from pharmacy.main import get_all_category
from pharmacy.methods.toolbar_buttons import ToolbarMixin
# from pharmacy.helper_pharmacy import search_drugs_apteka911
from pharmacy.models import Drug_apteka911, CategoryApteka911
from ui.mixins.htmx import HTMXTemplateMixin
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.mixins.section import AppSectionMetaMixin

list_pharmacy = {
    'apteka911': 'Аптека 911',
    'add': 'Аптека доброго дня',
    '1sa': 'Перша соціальна аптека',
}


class PharmacyBaseView(AppSectionMetaMixin):
    app_label = 'pharmacy'
    toolbar_buttons: list[str] = []
    # toolbar_buttons = ['update_categories', 'update_drugs']

    def get_section_config(self):
        if not self.app_label:
            raise ValueError("app_label is required")
        return apps.get_app_config(self.app_label)

    # def get_toolbar_buttons(self):
    #     return []  # Заглушка, щоб не було помилки

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # ctx.update({
        #     'toolbar_buttons': self.get_toolbar_buttons(),
        # })
        return ctx


class PharmacyUpdateDB(PharmacyBaseView, HTMXTemplateMixin, TemplateView):
    page_content = ('pharmacy.html',)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # drugs = get_all_drugs()
        # save_drugs(drugs)
        today = timezone.now().date()
        print(f'today: {Drug_apteka911.objects
              .filter(time_updated__lte=today)
              .order_by('-time_updated')
              .first()}')
        ctx['update'] = {

        }
        return ctx

class PharmacyUpdateCategory(PharmacyBaseView, HTMXTemplateMixin, ToolbarMixin, TemplateView):
    # page_content = ('pharmacy.html',)

    def get_queryset(self):
        # отримати категорії зі сторінки сайту
        categories = get_categories_whith_page_cite_apteka911()

        # оновити категорії в БД
        update_category(categories)
        
        # 

        query = self.request.POST.get('search_query') or self.request.GET.get('search_query', '')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        categories = get_categories_whith_page_cite_apteka911()
        # get_categories_with_sitemap(categories)
        update_category(categories)
        today = timezone.now().date()

        # ctx.update({
        #     'update_categories': today.strftime('%Y-%m-%d:%H-%M-%S'),
        # })

        return ctx






class PharmacyBasePageView(PharmacyBaseView, HTMXTemplateMixin, ToolbarMixin, TemplateView):
    page_content = ('pharmacy.html',)
    toolbar_buttons = ['update_categories', 'update_drugs']

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
            'toolbar_buttons': self.get_toolbar_buttons(),
        })

        return ctx


class PharmacyListDrugsView(PharmacyBaseView, HTMXTemplateMixin, ListView):
    model = Drug_apteka911
    # template_name = "base_table.html" # HTMX поверне тільки цей фрагмент
    htmx_template_name = 'list_drugs.html'

    # context_object_name = 'table' # Щоб base_table.html бачив дані як 'table'

    def post(self, request, *args, **kwargs):
        # Викликаємо метод get, щоб ListView відпрацював логіку
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        # Дістаємо query з POST (якщо форма відправлена) або з GET
        query = self.request.POST.get('search_query') or self.request.GET.get('search_query', '')
        # if query:
        #     return search_drugs_apteka911(query)
        #     # return self.model.objects.filter(name__icontains=query)
        # return self.model.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'word_search': self.request.POST.get('search_query', ''),
            'drugs': self.queryset,
        })
        return ctx
