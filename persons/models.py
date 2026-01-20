from django.utils import timezone

from django.db import models



class Person(models.Model):
    """ модель для довідника Фізичні Особи """
    GENDER_CHOICES = {
        'ч': 'чоловіча',
        'ж': 'жіноча',
    }
    last_name = models.CharField(max_length=100, name='Прізвище')
    first_name = models.CharField(max_length=100, name="Ім'я")
    patronymic = models.CharField(max_length=100, name='По батькові')  # по батькові
    # full_name = models.CharField(max_length=100, name='ПІБ')
    birth_date = models.DateField(blank=True, name='День народження')
    gender = models.CharField(choices=GENDER_CHOICES.items(), name='Стать')
    employee = models.BooleanField(name='Співробітник')
    is_working = models.BooleanField(default=False, name='Працює')
    time_create = models.DateTimeField(auto_now_add=True, name='Дата створення')
    time_update = models.DateTimeField(auto_now=True, name='Дата оновлення')

    @property
    def full_name(self):
        """ Returns the person's full name."""
        return f'{self.last_name} {self.first_name} {self.patronymic}'


class Orders(models.Model):
    """ модель для довідника Накази """
    number_order = models.CharField(max_length=8, name='Номер наказу')
    summary = models.TextField(max_length=200, blank=True, name='Короткий зміст')
    date_employment = models.DateTimeField(default=timezone.now, name='Дата прийняття')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)