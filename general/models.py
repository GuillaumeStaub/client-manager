from django.db import models
from datetime import date

def get_default_periode_name():
    pass

class InfosTechniques(models.Model):
    matricule_compteur = models.CharField(max_length=3, null=True, blank=True)
    num_armoire = models.CharField(max_length=5, verbose_name="numéro armoire")
    emplacement = models.CharField(max_length=2, default=0)

    def __str__(self):
        return f"{self.num_armoire} - {self.emplacement}"

    class Meta:
        unique_together = (('num_armoire', 'emplacement'),)
        verbose_name = 'Informations Techniques'
        verbose_name_plural = 'Informations Techniques'


class Saison(models.Model):
    pass
