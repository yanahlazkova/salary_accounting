from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Organization(models.Model):
    """ Дані організації (ЄДРПОУ, МФО, назва) """

    name = models.CharField(
        'Назва організації',
        max_length=500,
        # name='Назва установи'
    )
    edrpou = models.PositiveIntegerField(
        'ЄДРПОУ',
        max_length=8,
#         name='ЄДРПОУ',
    )
    mfo = models.PositiveIntegerField(
        'МФО',
        max_length=6,
#         name='МФО'
    )
    address = models.TextField(
        "Юридична адреса",
        blank=True
    )

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


class Ustanova(models.Model):
    name = models.CharField(max_length=500)
    kpk = models.PositiveIntegerField(
        max_length=7,
        verbose_name='КПК')

    class Meta:
        verbose_name = 'Налаштування установи'
        verbose_name_plural = 'Налаштування установи'

    def __str__(self):
        return self.kpk

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


class KEKV(models.Model):
    name = models.PositiveSmallIntegerField(
        max_length=4,
        unique=True,
    )
    about = models.TextField(
        max_length=250,
        blank=True,
        null=True,
    )