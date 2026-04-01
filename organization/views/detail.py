from organization.forms import UstanovaForm
from organization.models import Ustanova, BankAccount, Department
from organization.views.base import SettingsOrgBaseView
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.dashboard import BlockTable
from ui.views.detail import UIDetailView
from ui.views.helper import get_table_data


class SettingsUstanovaDetailView(SettingsOrgBaseView, SectionPageToolbarMixin, UIDetailView):
    model = Ustanova
    toolbar_buttons = ['exit', 'edit_ust']

    accounts_block = BlockTable()
    departments_block = BlockTable()

    slug_field = 'kpk'
    slug_url_kwarg = 'kpk'

    form_class = UstanovaForm

    def get_accounts_block(self):
        # self.accounts_block = BlockTable()
        self.accounts_block.app_label = self.app_label

        self.accounts_block.model = BankAccount

        self.accounts_block.slug_field = 'account'
        self.accounts_block.slug_url_kwarg = 'account'
        accounts = BankAccount.objects.filter(ustanova=self.object) #.values()

        self.accounts_block.name = self.get_page_subtitle('table_accounts')
        self.accounts_block.table_titles = self.accounts_block.get_table_titles()
        revers_url = 'organization:view_account'
        self.accounts_block.table_rows = get_table_data(self.accounts_block, revers_url=revers_url, queryset=accounts)
        self.accounts_block.toolbar_buttons = ['create_account']
        self.accounts_block.toolbar_buttons = self.accounts_block.get_toolbar_buttons(
            extra_kwargs={'kpk': self.object.kpk}
        )

        return self.accounts_block


    def get_departments_block(self):
        # self.departments_block = BlockTable()
        self.departments_block.app_label = self.app_label

        self.departments_block.model = Department

        self.departments_block.slug_field = 'pk'
        self.departments_block.slug_url_kwarg = 'pk'

        self.departments_block.name = self.get_page_subtitle('table_departments')
        self.departments_block.table_titles = self.departments_block.get_table_titles()

        departments = Department.objects.filter(ustanova=self.object) #.values()

        revers_url = 'organization:view_department'

        self.departments_block.table_rows = get_table_data(self.departments_block, revers_url=revers_url, queryset=departments)
        self.departments_block.toolbar_buttons = ['create_department']
        self.departments_block.toolbar_buttons = self.departments_block.get_toolbar_buttons(
            extra_kwargs={'kpk': self.object.kpk}
        )

        return self.departments_block


    def change_page_content(self):
        page_content = self.get_page_content()
        page_content[0] = 'ustanova_view.html'
        # page_content.append('base_table.html')

        return page_content

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'form_title': self.get_form_title('view_ust'),
            'page_content': self.change_page_content(),
            'accounts': self.get_accounts_block(),
            'departments': self.get_departments_block(),
        })
        # for c in ctx:
        #     print(f'{c}: {ctx[c]}')
        return ctx



""" 1-й варіант """
from django.urls import reverse

def get_context_data1(self, **kwargs):
    ctx = super().get_context_data(**kwargs)

    # 1. Отримуємо QuerySet
    departments_qs = Department.objects.filter(ustanova=self.object)

    # 2. Визначаємо список полів, які хочемо вивести (крім ID)
    # Можна вказати явно, або отримати всі автоматично
    included_fields = ['name', 'code', 'description']  # Замініть на ваші назви полів

    # 3. Формуємо заголовки (table_titles)
    # Беремо verbose_name кожного поля з метаданих моделі
    titles = [
        Department._meta.get_field(field).verbose_name
        for field in included_fields
    ]

    # 4. Формуємо рядки (table_rows)
    rows = []
    for dept in departments_qs:
        rows.append({
            # URL для HTMX (наприклад, перегляд відділу)
            'row_url': reverse('organization:department_view', kwargs={'pk': dept.pk}),

            # Дані рядка у форматі {поле: значення}
            'values': {
                field: getattr(dept, field) for field in included_fields
            }
        })

    # 5. Збираємо все в об'єкт table, як очікує шаблон
    ctx['table'] = {
        'table_titles': titles,
        'table_rows': rows
    }

    return ctx

""" 2-й варіант """

def get_context_data2(self, **kwargs):
    ctx = super().get_context_data(**kwargs)

    # 1. Отримуємо ваш QuerySet
    departments = Department.objects.filter(ustanova=self.object)

    # 2. Визначаємо, які саме поля ми хочемо бачити в таблиці
    # Наприклад: 'code' (код підрозділу) та 'name' (назва)
    fields_to_show = ['code', 'name']

    # 3. Автоматично витягуємо verbose_name для заголовків
    table_titles = []
    for field_name in fields_to_show:
        field = Department._meta.get_field(field_name)
        table_titles.append(field.verbose_name)

    # 4. Формуємо рядки для таблиці
    table_rows = []
    for dept in departments:
        values_dict = {}
        for field_name in fields_to_show:
            # Отримуємо значення поля
            value = getattr(dept, field_name)

            # Якщо це поле з choices, красиво виведемо його текст, а не ключ
            if hasattr(dept, f'get_{field_name}_display'):
                value = getattr(dept, f'get_{field_name}_display')()

            values_dict[field_name] = value

        # Додаємо 'id', якщо ваш шаблон або HTMX його використовує
        values_dict['id'] = dept.id

        table_rows.append({
            # Генеруємо URL для переходу на цей підрозділ
            'row_url': reverse('organization:department_detail', kwargs={'pk': dept.pk}),
            'values': values_dict
        })

    # 5. Пакуємо все в один словник 'table', як того вимагає ваш HTML
    ctx['table'] = {
        'table_titles': table_titles,
        'table_rows': table_rows
    }

    return ctx