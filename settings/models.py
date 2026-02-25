from decimal import Decimal

from django.core.validators import MinValueValidator, DecimalValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class SocialSettings(models.Model):
    """
    Соціальні стандарти, що діють з певної дати.
    Кожен новий запис позначає зміну законодавства.
    """
    effective_from = models.DateField(
        verbose_name="Діє з (дата)",
        unique=True,
        help_text='Оберіть дату, з якої ці показники стають актуальними.',
        error_messages={
            'unique': 'Показник з такою датою вже існує',
        }
    )

    # Показники
    min_salary = models.DecimalField(max_digits=10, decimal_places=2,
                                     validators=[MinValueValidator(Decimal('0.01'))],  # Мінімальне значення — 1 копійка
                                     verbose_name="Мінімальна заробітна плата (місячна)", default=1000.00)
    pm_able_bodied = models.DecimalField(max_digits=10, decimal_places=2,
                                         # Мінімальне значення — 1 копійка
                                         validators=[MinValueValidator(Decimal('0.01'))],
                                         verbose_name="Прожитковий мінімум (працездатні)", default=1000.00)

    # Ставки податків
    pdfo_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                    validators=[
                                        MinValueValidator(Decimal('0.01'), message='Ви впевненні, що значення більше 0,00?'), # Мінімальне значення — 1 копійка
                                        MaxValueValidator(Decimal('99.99'), message='Ви впевненні, що значення менше 100?')
                                    ],
                                    verbose_name="Ставка ПДФО, %", default=18.0, )
    vz_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                  validators=[MinValueValidator(Decimal('0.01'))],  # Мінімальне значення — 1 копійка
                                  verbose_name="Військовий збір, %", default=1.5,)

    esv_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                   validators=[MinValueValidator(Decimal('0.01'))],  # Мінімальне значення — 1 копійка
                                   verbose_name="ЄСВ, %", default=22.0)
    # esv_invalid_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="ЄСВ (інвалідність)",
    #                                        validators=[MinValueValidator(Decimal('0.01'))],
    #                                        # Мінімальне значення — 1 копійка
    #                                        default=8.41)

    # Дати створення/оновлення запису
    time_created = models.DateTimeField(auto_now_add=True)  # дата при створенні запису
    time_updated = models.DateTimeField(auto_now=True)  # дата при зміні запису
    # user_created - користувач, який створив запис
    # user_updated - останній користувач, який змінив запис

    def __str__(self):
        return str(self.effective_from)

    def get_absolute_url(self):
        """ щоб після будь-якої дії з об'єктом (створення, редагування) Django знав, куди "йти" """
        return reverse('settings:view', kwargs={'date': self.effective_from})

    class Meta:
        db_table = 'social_settings'
        ordering = ['-effective_from']