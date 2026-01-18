from django.db import models

from django.db import models


class PositionClassifier(models.Model):
    """
    Класифікатор професій (ДК 003:2010).
    Використовується для офіційного кадрового обліку та звітності.
    """

    code_kp = models.CharField(
        max_length=15,
        verbose_name="Код КП",
        help_text="Код за класифікатором професій (напр. 2411.2)"
    )

    code_zkpptr = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Код ЗКППТР",
        help_text="Код загальносоюзного класифікатора (якщо є)"
    )

    name = models.CharField(
        max_length=500,
        verbose_name="Професійна назва роботи"
    )

    class Meta:
        verbose_name = "Класифікатор посад"
        verbose_name_plural = "Класифікатор посад (ДК 003:2010)"
        ordering = ['code_kp']
        # Додаємо індекс для швидкого пошуку за кодом та назвою
        indexes = [
            models.Index(fields=['code_kp']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.code_kp} — {self.name}"
