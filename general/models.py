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

    def save(self, *args, **kwarg):
        self.prix_ttc = round(self.prix_ht * (1 + self.taxe / 100), 2)
        super(Forfait, self).save(*args, **kwarg)

    def __str__(self):
        return f"{self.nom}"


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=60)
    adresse = models.CharField(max_length=250)
    code_postal = models.CharField(max_length=5)
    commune = models.CharField(max_length=100)
    societe_manege = models.CharField(max_length=150, blank=True, null=True, verbose_name="Société - Manège")
    telephone = models.CharField(max_length=10)
    email = models.EmailField(max_length=250, null=True, blank=True)

    class Meta:
        ordering = ['nom', 'prenom']
        unique_together = (('nom', 'societe_manege'),)

    def __str__(self):
        if self.societe_manege:
            return f"{self.societe_manege}"
        else:
            return f"{self.nom} {self.prenom}"


class Evenement(models.Model):
    TYPE_CHOICES = (
        (1, "Fête foraine"),
        (2, "Brocante"),
        (3, "Cirque"),
        (4, "Autre")
    )
    nom = models.CharField(max_length=250)
    ville = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="Type d'évènement")

    class Meta:
        verbose_name = "Evènement"
        verbose_name_plural = "Evènements"

    def __str__(self):
      return f"{self.nom} à {self.ville}"

class Commande(models.Model):
    saison = models.ForeignKey(Saison, on_delete=models.PROTECT)
    evenement = models.ForeignKey(Evenement, on_delete=models.PROTECT)
    puissance = models.IntegerField(default=0, help_text='Puissance en KvA', )
    forfait = models.ForeignKey(Forfait, on_delete=models.PROTECT)
    nb_jours = models.IntegerField(default=23, verbose_name='Nombre de jours')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    infos_techniques = models.ForeignKey(InfosTechniques, null=True, on_delete=models.PROTECT,
                                         verbose_name="Informations techniques")
    total_ht = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    total_ttc = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    payee = models.BooleanField(default=False, verbose_name='Commade payée')

    def save(self, *args, **kwarg):
        self.total_ht = round(self.forfait.prix_ht * self.nb_jours, 2)
        self.total_ttc = round(self.forfait.prix_ht * (1 + self.forfait.taxe / 100) * self.nb_jours, 2)
        super(Commande, self).save(*args, **kwarg)

    def __str__(self):
        if self.client.societe_manege:
            return f"{self.saison} - {self.client.societe_manege}"
        else:
            return f"{self.saison} - {self.client.nom} {self.client.prenom}"
