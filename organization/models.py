from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Organization(models.Model):
    """ Дані організації (ЄДРПОУ, МФО, назва) """

    name = models.CharField(
        verbose_name='Назва організації',
        max_length=500,
        # name='Назва установи'
    )
    edrpou = models.CharField(
        verbose_name='ЄДРПОУ',
        max_length=8,
        unique=True,
#         name='ЄДРПОУ',
    )
    mfo = models.PositiveIntegerField(
        verbose_name='МФО',
#         name='МФО'
    )
    address = models.TextField(
        verbose_name="Юридична адреса",
        blank=True
    )
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')  # дата при створенні запису
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')  # дата при зміні запису

    # user_created - користувач, який створив запис
    # user_updated - останній користувач, який змінив запис


    class Meta:
        verbose_name = "Налаштування організації"
        verbose_name_plural = "Налаштування організації"

    def save(self, *args, **kwargs):
        # Забороняємо створювати більше одного запису
        if not self.pk and Organization.objects.exists():
            raise ValidationError("Можна створити лише один запис з налаштуваннями.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ щоб після будь-якої дії з об'єктом (створення, редагування) Django знав, куди "йти" """
        return reverse('organization:settings')


class Ustanova(models.Model):
    name = models.CharField(max_length=500,
                            verbose_name='Назва установи')
    kpk = models.PositiveIntegerField(
        unique=True,
        verbose_name='КПК')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')  # дата при створенні запису
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')  # дата при зміні запису

    # user_created - користувач, який створив запис
    # user_updated - останній користувач, який змінив запис


    class Meta:
        verbose_name = 'Установа'
        verbose_name_plural = 'Установи'

    def __str__(self):
        return f"{self.name} ({self.kpk})"

    def get_absolute_url(self):
        """ щоб після будь-якої дії з об'єктом (створення, редагування) Django знав, куди "йти" """
        return reverse('organization:settings')


class BankAccount(models.Model):

    FUND_CHOICES = {
        'general_fund': 'Загальний фонд',
        'special_fund': 'Спеціальний фонд',
    }

    account = models.CharField(
        max_length=500,
        verbose_name='Рахунок',
        db_comment='Рахунок в форматі IBAN',
        unique=True,
    )
    fund = models.CharField(
        choices=FUND_CHOICES,
        verbose_name='Фонд коштів',
        db_comment='Назва фонду коштів (загальний, спецкошти)'
    )
    ustanova = models.ForeignKey(
        Ustanova,
        on_delete=models.CASCADE,
        db_comment='Установа, якій належить рахунок',
        related_name='bank_accounts',
        related_query_name='bank_account',
        null=True,
        blank=True,
    )
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')  # дата при створенні запису
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')  # дата при зміні запису
    # user_created - користувач, який створив запис
    # user_updated - останній користувач, який змінив запис


class KEKV(models.Model):
    name = models.PositiveSmallIntegerField(
        unique=True,
    )
    about = models.TextField(
        blank=True,
        null=True,
    )