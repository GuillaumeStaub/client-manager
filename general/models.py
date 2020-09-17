from django.db import models
from datetime import datetime, timedelta
from client_manager.settings import MONTHS


def get_default_periode_name():
    """
    Methode  give a default value to the name of a season
    :return: (str) Formatted Date
    """
    name = (str(datetime.now()).split('-'))
    month = MONTHS[int(name[1]) - 1]
    return f'{name[0]} - {month}'


def get_default_interval():
    """
    Methode  give a default value to the date_fin Saison field
    :return: (datetime) Today date plus 23 days
    """
    return datetime.now() + timedelta(days=23)


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
    nom = models.CharField(max_length=50, default=get_default_periode_name, primary_key=True)
    date_debut = models.DateField(default=datetime.now, verbose_name='Début de la saison')
    date_fin = models.DateField(default=get_default_interval, verbose_name='Fin de la saison')
    nb_jours = models.IntegerField(default=23, verbose_name='Nombre de jours')

    class Meta:
        verbose_name_plural = "Périodes"
        verbose_name = "Période"

    def __str__(self):
        return self.nom


class Forfait(models.Model):
    nom = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()
    prix_ht = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Prix HT')
    prix_ttc = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Prix TTC')
    taxe = models.DecimalField(max_digits=4, decimal_places=2, default=20.00)
    saison = models.ForeignKey(Saison, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nom}"
