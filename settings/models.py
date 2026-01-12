from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PayrollSettings(models.Model):
    """
    Глобальні налаштування та соціальні показники для розрахунку зарплати.
    """
    year = models.PositiveIntegerField(
        verbose_name="Рік",
        default=2025
    )
    min_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Мінімальна ЗП (місячна), грн",
        default=8000.00
    )
    pm_for_able_bodied = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Прожитковий мінімум для працездатних осіб, грн",
        default=3028.00
    )
    pdfo_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Ставка ПДФО, %",
        default=18.00
    )
    vz_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Ставка Військового збору, %",
        default=5.00
    )
    esv_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Ставка ЄСВ, %",
        default=22.00
    )
    """ дата початку дії"""
    time_start = models.DateField(

    )

    class Meta:
        verbose_name = "Налаштування показників"
        verbose_name_plural = "Налаштування показників"

    def __str__(self):
        return f"Налаштування на {self.year} рік"

    # Метод для обмеження створення більше ніж одного запису
    def save(self, *args, **kwargs):
        if not self.pk and PayrollSettings.objects.exists():
            return # Або викинути помилку, щоб не створювати дублікати
        return super().save(*args, **kwargs)