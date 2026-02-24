from django.db import models


class Ustanova(models.Model):
    """ Дані установи (ЄДРПОУ, МФО, назва) """

    name = models.CharField(max_length=500, name='Назва установи')
    edrpou = models.IntegerField(max_length=8, name='ЄДРПОУ')
    mfo = models.IntegerField(max_length=6, name='МФО')
