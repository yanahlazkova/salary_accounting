from django.db import models


class Drug(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва препарату")
    code = models.CharField(max_length=50, unique=True)  # Наприклад: p12181
    alias = models.CharField(max_length=255)  # Наприклад: /shop/asparkam-p12181
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name