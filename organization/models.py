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
                            unique=True,
                            verbose_name='Назва установи')
    short_name = models.CharField(max_length=20,
                                  verbose_name='Скорочена назва',
                                  # blank=True,
                                  # null=True,
                                  default=name,
                                  )
    kpk = models.PositiveIntegerField(
        verbose_name='КПК')

    head = models.CharField(max_length=500,
                            verbose_name='Керівник',
                            blank=True,
                            null=True,
                            # default='-',
                            )
    # location = models.CharField(
    #     max_length=500,
    #     verbose_name='Розташування',
    #     null=True,
    #
    # )
    # address = models.TextField(verbose_name='адреса', blank=False, null=True)

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
        return reverse(f'organization:view_ust', kwargs={'kpk': self.kpk})



class Department(models.Model):
    name = models.CharField(max_length=500,
                            unique=True,
                            verbose_name='Назва підгрупи')
    ustanova = models.ForeignKey(
        Ustanova,
        verbose_name='Установа',
        on_delete=models.CASCADE,
        db_comment='Установа, якій підпорядковується підгрупа',
        related_name='ustanova',
        related_query_name='ustanovas',
        # null=True,
        # blank=True,
    )

    head = models.CharField(max_length=500,
                            verbose_name='Керівник',
                            blank=True,
                            null=True,
                            )
    location = models.CharField(
        max_length=500,
        verbose_name='Розташування',
        null=True,
    )
    # address = models.TextField(verbose_name='Адреса', blank=False, null=True)

    time_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Дата створення')  # дата при створенні запису
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')  # дата при зміні запису

    # user_created - користувач, який створив запис
    # user_updated - останній користувач, який змінив запис


    class Meta:
        verbose_name = 'Підрозділ'
        verbose_name_plural = 'Підрозділ'

    def __str__(self):
        return f"{self.name} ({self.ustanova.kpk})"

    def get_absolute_url(self):
        """ щоб після будь-якої дії з об'єктом (створення, редагування) Django знав, куди "йти" """
        return reverse(f'organization:view_ust', kwargs={'kpk': self.ustanova.kpk})


class BankAccount(models.Model):
    FUND_CHOICES = {
        '': '- Дані не вибрані -',
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
        verbose_name='Фонд виду коштів',
        db_comment='Назва фонду коштів (загальний, спецкошти)',
        # default='Рахунок не обраний'
    )
    ustanova = models.ForeignKey(
        Ustanova,
        verbose_name='Установа',
        on_delete=models.CASCADE,
        db_comment='Установа, якій належить рахунок',
        related_name='bank_accounts',
        related_query_name='bank_account',
        # null=True,
        # blank=True,
        default=1
    )
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')  # дата при створенні запису
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')  # дата при зміні запису
    # user_created - користувач, який створив запис
    # user_updated - останній користувач, який змінив запис

    def get_absolute_url(self):
        """ щоб після будь-якої дії з об'єктом (створення, редагування) Django знав, куди "йти" """
        return reverse(f'organization:view_ust', kwargs={'kpk': self.ustanova.kpk})



class KEKV(models.Model):
    name = models.PositiveSmallIntegerField(
        unique=True,
    )
    about = models.TextField(
        blank=True,
        null=True,
    )
