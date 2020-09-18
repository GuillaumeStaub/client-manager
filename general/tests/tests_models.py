from django.test import TestCase
from general.models import InfosTechniques, Saison, get_default_periode_name, get_default_interval, Forfait, Client, \
    Commande, Evenement
from datetime import timedelta, datetime
from freezegun import freeze_time
from django.db import IntegrityError

FAKE_TIME = datetime(2020, 9, 16, 17, 5, 55)
FAKE_TIME_INTERVAL = FAKE_TIME + timedelta(days=23)


class InfosTechniquesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        InfosTechniques.objects.create(matricule_compteur='673', num_armoire='CH01')

    def test_matricule_compteur_label(self):
        infos_techniques = InfosTechniques.objects.get(id=1)
        field_label = infos_techniques._meta.get_field('matricule_compteur').verbose_name
        assert field_label == 'matricule compteur'

    def test_num_armoie_label(self):
        infos_techniques = InfosTechniques.objects.get(id=1)
        field_label = infos_techniques._meta.get_field('num_armoire').verbose_name
        assert field_label == 'numéro armoire'

    def test_emplacement_label(self):
        infos_techniques = InfosTechniques.objects.get(id=1)
        field_label = infos_techniques._meta.get_field('emplacement').verbose_name
        assert field_label == 'emplacement'

    def test_matricule_compteur_length(self):
        infos_techniques = InfosTechniques.objects.get(id=1)
        max_length = infos_techniques._meta.get_field('matricule_compteur').max_length
        assert max_length == 3

    def test_num_armoire_length(self):
        infos_techniques = InfosTechniques.objects.get(id=1)
        max_length = infos_techniques._meta.get_field('num_armoire').max_length
        assert max_length == 5

    def test_emplacement_length(self):
        infos_techniques = InfosTechniques.objects.get(id=1)
        max_length = infos_techniques._meta.get_field('emplacement').max_length
        assert max_length == 2

    def test_emplacement_0_is_default_value(self):
        infos_techniques = InfosTechniques.objects.get(id=1)
        default_value = infos_techniques._meta.get_field('emplacement').default
        assert default_value == 0

    def test_num_armoire_null_and_blank_true(self):
        raised = False
        try:
            InfosTechniques.objects.create(num_armoire='CH01', emplacement=2)
        except:
            raised = True
        assert raised == False

    def test_object_verbose_name_plural(self):
        infos_techniques = InfosTechniques.objects.get(id=1)
        verbose_name_plural = infos_techniques._meta.verbose_name_plural
        assert verbose_name_plural == "Informations Techniques"

    def test_object_name_is_num_armoire_dash_emplacement(self):
        infos_techniques = InfosTechniques.objects.get(id=1)
        expected_object_name = f'{infos_techniques.num_armoire} - {infos_techniques.emplacement}'
        assert expected_object_name == str(infos_techniques)


class SaisonModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Saison.objects.create(nom='2020 - Septembre')

    @freeze_time(FAKE_TIME)
    def test_get_default_saison_name(self):
        assert get_default_periode_name() == '2020 - Septembre'

    @freeze_time(FAKE_TIME)
    def test_get_default_interval(self):
        assert get_default_interval() == FAKE_TIME_INTERVAL

    def test_nom_label(self):
        saison = Saison.objects.get(nom='2020 - Septembre')
        field_label = saison._meta.get_field('nom').verbose_name
        assert field_label == 'nom'

    def test_date_debut_label(self):
        saison = Saison.objects.get(nom='2020 - Septembre')
        field_label = saison._meta.get_field('date_debut').verbose_name
        assert field_label == 'Début de la saison'

    def test_date_fin_label(self):
        saison = Saison.objects.get(nom='2020 - Septembre')
        field_label = saison._meta.get_field('date_fin').verbose_name
        assert field_label == 'Fin de la saison'

    def test_nb_jours_label(self):
        saison = Saison.objects.get(nom='2020 - Septembre')
        field_label = saison._meta.get_field('nb_jours').verbose_name
        assert field_label == 'Nombre de jours'

    def test_nom_length(self):
        saison = Saison.objects.get(nom='2020 - Septembre')
        max_length = saison._meta.get_field('nom').max_length
        assert max_length == 50

    @freeze_time(datetime(2020, 10, 16, 17, 5, 55))
    def test_nom_format_default_value(self):
        saison = Saison.objects.create()
        default_value = saison._meta.get_field('nom').default
        assert default_value() == '2020 - Octobre'

    def test_date_debut_date_now_is_default_value(self):
        with freeze_time(FAKE_TIME) as frozen_datetime:
            saison = Saison.objects.get(nom='2020 - Septembre')
            default_value = saison._meta.get_field('date_debut').default
            assert frozen_datetime() == FAKE_TIME

    @freeze_time(FAKE_TIME)
    def test_date_debut_fin_now_timedelta_30_is_default_value(self):
        saison = Saison.objects.get(nom='2020 - Septembre')
        default_value = saison._meta.get_field('date_fin').default
        assert default_value() == FAKE_TIME + timedelta(23)

    def test_date_nb_jours_23_is_default_value(self):
        saison = Saison.objects.get(nom='2020 - Septembre')
        default_value = saison._meta.get_field('nb_jours').default
        assert default_value == 23

    def test_object_verbose_name_plural(self):
        saison = Saison.objects.get(nom='2020 - Septembre')
        verbose_name_plural = saison._meta.verbose_name_plural
        assert verbose_name_plural == "Périodes"

    def test_object_name_is_nom(self):
        saison = Saison.objects.get(nom='2020 - Septembre')
        expected_object_name = f'{saison.nom}'
        assert expected_object_name == str(saison.nom)


class ForfaitModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        saison = Saison.objects.create(nom='2020 - Septembre')
        Forfait.objects.create(nom='Forfait 1', description='Puissance inférieure à 18kVA', prix_ht=14.17, taxe=20.00,
                               saison=saison)

    def test_nom_label(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        field_label = forfait._meta.get_field('nom').verbose_name
        assert field_label == 'nom'

    def test_description_label(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        field_label = forfait._meta.get_field('description').verbose_name
        assert field_label == 'description'

    def test_prix_ht_label(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        field_label = forfait._meta.get_field('prix_ht').verbose_name
        assert field_label == 'Prix HT'

    def test_taxe_label(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        field_label = forfait._meta.get_field('taxe').verbose_name
        assert field_label == 'taxe'

    def test_prix_ttc_label(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        field_label = forfait._meta.get_field('prix_ttc').verbose_name
        assert field_label == 'Prix TTC'

    def test_nom_length(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        max_length = forfait._meta.get_field('nom').max_length
        assert max_length == 100

    def test_prix_ht_max_digits(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        max_digits = forfait._meta.get_field('prix_ht').max_digits
        assert max_digits == 6

    def test_prix_ht_decimal_places(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        decimal_places = forfait._meta.get_field('prix_ht').decimal_places
        assert decimal_places == 2

    def test_taxe_max_digits(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        max_digits = forfait._meta.get_field('taxe').max_digits
        assert max_digits == 4

    def test_taxe_decimal_places(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        decimal_places = forfait._meta.get_field('taxe').decimal_places
        assert decimal_places == 2

    def test_taxe_default_value_is_20(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        default_value = forfait._meta.get_field('taxe').default
        assert default_value == 20.00

    def test_prix_ttc_max_digits(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        max_digits = forfait._meta.get_field('prix_ttc').max_digits
        assert max_digits == 7

    def test_prix_ttc_decimal_places(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        decimal_places = forfait._meta.get_field('prix_ttc').decimal_places
        assert decimal_places == 2

    def test_object_name_is_nom(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        expected_object_name = f'{forfait.nom}'
        assert expected_object_name == str(forfait)

    def test_prix_ttc_correctly_save(self):
        forfait = Forfait.objects.get(nom='Forfait 1')
        assert forfait.prix_ttc == round(forfait.prix_ht * (1 + forfait.taxe / 100), 2)


class ClientModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Client.objects.create(nom='Villard', prenom='Jean', adresse='13 rue de la paix', code_postal=75000,
                              commune='Paris', telephone='0600112233', email='jean.villard@yahooo.com',
                              societe_manege='Rambo')

    def test_nom_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('nom').verbose_name
        assert field_label == 'nom'

    def test_prenom_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('prenom').verbose_name
        assert field_label == 'prenom'

    def test_adresse_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('adresse').verbose_name
        assert field_label == 'adresse'

    def test_code_postal_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('code_postal').verbose_name
        assert field_label == 'code postal'

    def test_commune_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('commune').verbose_name
        assert field_label == 'commune'

    def test_societe_manege_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('societe_manege').verbose_name
        assert field_label == 'Société - Manège'

    def test_telephone_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('telephone').verbose_name
        assert field_label == 'telephone'

    def test_email_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('email').verbose_name
        assert field_label == 'email'

    def test_nom_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('nom').max_length
        assert max_length == 100

    def test_prenom_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('prenom').max_length
        assert max_length == 60

    def test_adresse_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('adresse').max_length
        assert max_length == 250

    def test_code_postal_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('code_postal').max_length
        assert max_length == 5

    def test_commune_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('commune').max_length
        assert max_length == 100

    def test_societe_manege_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('societe_manege').max_length
        assert max_length == 150

    def test_telephone_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('telephone').max_length
        assert max_length == 10

    def test_email_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('email').max_length
        assert max_length == 250

    def test_nom_societe_manege_email_null_and_blank_true(self):
        raised = False
        try:
            Client.objects.create(nom='Jean', prenom='Paul', adresse='13 rue de la paix', code_postal=75000,
                                  commune='Paris', telephone='0600112233')
        except:
            raised = True
        assert raised == False

    def test_nom_and_societe_manege_unique_together(self):
        with self.assertRaises(IntegrityError):
            Client.objects.create(nom='Villard', prenom='Jean', adresse='13 rue de la paix', code_postal=75000,
                                  commune='Paris', telephone='0600112233', email='jean.villard@yahooo.com',
                                  societe_manege='Rambo')

    def test_object_name_is_societe_manege_if_true(self):
        client = Client.objects.get(id=1)
        expected_object_name = f'{client.societe_manege}'
        assert expected_object_name == str(client)

    def test_object_name_is_nom_prenom_if_not_societe_manege(self):
        client = Client.objects.create(nom='Michel', prenom='René', adresse='13 rue de la paix', code_postal=75000,
                                       commune='Paris', telephone='0600112233')
        expected_object_name = f'{client.nom} {client.prenom}'
        assert expected_object_name == str(client)


class EvenementModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Evenement.objects.create(nom='Foire aux plaisirs', ville='Bordeaux', type='Fête foraine')

    def test_nom_label(self):
        event = Evenement.objects.get(id=1)
        field_label = event._meta.get_field('nom').verbose_name
        assert field_label == 'nom'

    def test_ville_label(self):
        event = Evenement.objects.get(id=1)
        field_label = event._meta.get_field('ville').verbose_name
        assert field_label == 'ville'

    def test_type_label(self):
        event = Evenement.objects.get(id=1)
        field_label = event._meta.get_field('type').verbose_name
        assert field_label == "Type d'évènement"

    def test_nom_length(self):
        event = Evenement.objects.get(id=1)
        max_length = event._meta.get_field('nom').max_length
        assert max_length == 250

    def test_ville_length(self):
        event = Evenement.objects.get(id=1)
        max_length = event._meta.get_field('ville').max_length
        assert max_length == 100

    def test_type_length(self):
        event = Evenement.objects.get(id=1)
        max_length = event._meta.get_field('type').max_length
        assert max_length == 50

    def test_object_name_is_nom_ville(self):
        event = Evenement.objects.get(id=1)
        expected_object_name = f'{event.nom} à {event.ville}'
        assert expected_object_name == str(event)

    def test_object_verbose_name_plural(self):
        event = Evenement.objects.get(id=1)
        verbose_name_plural = event._meta.verbose_name_plural
        assert verbose_name_plural == "Evènements"


class CommandeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        infos_techniques = InfosTechniques.objects.create(matricule_compteur='673', num_armoire='CH01')
        saison = Saison.objects.create(nom='2020 - Septembre')
        forfait = Forfait.objects.create(nom='Forfait 1', description='Puissance inférieure à 18kVA', prix_ht=14.17,
                                         taxe=20.00,
                                         prix_ttc=17.00, saison=saison)
        client = Client.objects.create(nom='Villard', prenom='Jean', adresse='13 rue de la paix', code_postal=75000,
                                       commune='Paris', telephone='0600112233', email='jean.villard@yahooo.com',
                                       societe_manege='Rambo')
        event = Evenement.objects.create(nom='Foire aux plaisirs', ville='Bordeaux', type='Fête foraine')
        Commande.objects.create(saison=saison, puissance=18, forfait=forfait, nb_jours=23, client=client,
                                infos_techniques=infos_techniques, evenement=event)

    def test_saison_label(self):
        commande = Commande.objects.get(id=1)
        field_label = commande._meta.get_field('saison').verbose_name
        assert field_label == 'saison'

    def test_puissance_label(self):
        commande = Commande.objects.get(id=1)
        field_label = commande._meta.get_field('puissance').verbose_name
        assert field_label == 'puissance'

    def test_forfait_label(self):
        commande = Commande.objects.get(id=1)
        field_label = commande._meta.get_field('forfait').verbose_name
        assert field_label == 'forfait'

    def test_nb_jours_label(self):
        commande = Commande.objects.get(id=1)
        field_label = commande._meta.get_field('nb_jours').verbose_name
        assert field_label == 'Nombre de jours'

    def test_infos_techniques_label(self):
        commande = Commande.objects.get(id=1)
        field_label = commande._meta.get_field('infos_techniques').verbose_name
        assert field_label == 'Informations techniques'

    def test_total_ht_label(self):
        commande = Commande.objects.get(id=1)
        field_label = commande._meta.get_field('total_ht').verbose_name
        assert field_label == 'total ht'

    def test_total_ttc_label(self):
        commande = Commande.objects.get(id=1)
        field_label = commande._meta.get_field('total_ttc').verbose_name
        assert field_label == 'total ttc'

    def test_payee_label(self):
        commande = Commande.objects.get(id=1)
        field_label = commande._meta.get_field('payee').verbose_name
        assert field_label == 'Commade payée'

    def test_total_ht_digits(self):
        commande = Commande.objects.get(id=1)
        max_digits = commande._meta.get_field('total_ht').max_digits
        assert max_digits == 6

    def test_total_ht_decimal(self):
        commande = Commande.objects.get(id=1)
        decimal_places = commande._meta.get_field('total_ht').decimal_places
        assert decimal_places == 2

    def test_total_ttc_digits(self):
        commande = Commande.objects.get(id=1)
        max_digits = commande._meta.get_field('total_ttc').max_digits
        assert max_digits == 6

    def test_total_ttc_decimal(self):
        commande = Commande.objects.get(id=1)
        decimal_places = commande._meta.get_field('total_ttc').decimal_places
        assert decimal_places == 2

    def test_total_ht_and_total_ttc_correctly_save(self):
        commande = Commande.objects.get(id=1)
        assert commande.total_ht == round(commande.forfait.prix_ht * commande.nb_jours, 2)
        assert commande.total_ttc == round(
            (commande.forfait.prix_ht * (1 + commande.forfait.taxe / 100)) * commande.nb_jours, 2)

    def test_object_name_is_saison_dash_societe_manege_if_true(self):
        commande = Commande.objects.get(id=1)
        expected_object_name = f'{commande.saison} - {commande.client.societe_manege}'
        assert expected_object_name == str(commande)

    def test_puissance_default_value_is_0(self):
        commande = Commande.objects.get(id=1)
        default_value = commande._meta.get_field('puissance').default
        assert default_value == 0

    def test_nb_jours_default_value_is_23(self):
        commande = Commande.objects.get(id=1)
        default_value = commande._meta.get_field('nb_jours').default
        assert default_value == 23

    def test_total_ht_default_value_is_0(self):
        commande = Commande.objects.get(id=1)
        default_value = commande._meta.get_field('total_ht').default
        assert default_value == 0

    def test_total_ttc_default_value_is_0(self):
        commande = Commande.objects.get(id=1)
        default_value = commande._meta.get_field('total_ttc').default
        assert default_value == 0

    def test_payee_default_value_is_false(self):
        commande = Commande.objects.get(id=1)
        default_value = commande._meta.get_field('payee').default
        assert default_value == False

    def test_object_name_is_saison_dash_client_nom_client_prenom(self):
        infos_techniques = InfosTechniques.objects.create(matricule_compteur='674', num_armoire='CH02')
        saison = Saison.objects.create(nom='2020 - Octobre')
        forfait = Forfait.objects.create(nom='Forfait 2', description='Puissance inférieure à 18kVA', prix_ht=14.17,
                                         taxe=20.00,
                                         prix_ttc=17.00, saison=saison)
        client = Client.objects.create(nom='Rodriguez', prenom='Jean', adresse='13 rue de la paix', code_postal=75000,
                                       commune='Paris', telephone='0600112233', email='jean.villard@yahooo.com', )
        event = Evenement.objects.create(nom='Brocante des Quinquonces', ville='Bordeaux', type='Brocante')
        commande = Commande.objects.create(saison=saison, puissance=18, forfait=forfait, nb_jours=23, client=client,
                                           infos_techniques=infos_techniques, total_ht=325.91, total_ttc=391.00, evenement=event)
        expected_object_name = f'{commande.saison} - {commande.client.nom} {commande.client.prenom}'
        assert expected_object_name == str(commande)
