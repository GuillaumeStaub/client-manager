from django.test import TestCase
from general.models import InfosTechniques, Saison, get_default_periode_name
import pytest
import datetime
from datetime import timedelta

FAKE_TIME = datetime.datetime(2020, 9, 16, 17, 5, 55)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, 'datetime', mydatetime)


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
        expected_object_name == str(infos_techniques)


class SaisonModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Saison.objects.create(nom='2020 - Septembre')

    def test_get_default_periode_name(self):
        assert get_default_periode_name() == '2020 - Septembre'

    def test_get_default_periode_name(self):
        assert get_default_periode_name() == FAKE_TIME + timedelta(23)

    def test_nom_label(self):
        saison = Saison.objects.get(id='2020 - Septembre')
        field_label = saison._meta.get_field('nom').verbose_name
        assert field_label == 'nom'

    def test_date_debut_label(self):
        saison = Saison.objects.get(id='2020 - Septembre')
        field_label = saison._meta.get_field('date_debut').verbose_name
        assert field_label == 'Début de la saison'

    def test_date_fin_label(self):
        saison = Saison.objects.get(id='2020 - Septembre')
        field_label = saison._meta.get_field('date_fin').verbose_name
        assert field_label == 'Fin de la saison'

    def test_nb_jours_label(self):
        saison = Saison.objects.get(id='2020 - Septembre')
        field_label = saison._meta.get_field('nb_jours').verbose_name
        assert field_label == 'Nombre de jours'

    def test_nom_length(self):
        saison = Saison.objects.get(id='2020 - Septembre')
        max_length = saison._meta.get_field('nom').max_length
        assert max_length == 50

    def test_nom_format_default_value(self):
        saison = InfosTechniques.objects.create()
        default_value = saison._meta.get_field('nom').default
        assert default_value == '2020 - Septembre'

    def test_date_debut_date_now_is_default_value(self):
        saison = Saison.objects.get(id='2020 - Septembre')
        default_value = saison._meta.get_field('date_debut').default
        assert default_value == FAKE_TIME

    def test_date_debut_fin_now_timedelta_30_is_default_value(self):
        saison = Saison.objects.get(id='2020 - Septembre')
        default_value = saison._meta.get_field('date_fin').default
        assert default_value == FAKE_TIME + timedelta(23)

    def test_date_nb_jours_23_is_default_value(self):
        saison = Saison.objects.get(id='2020 - Septembre')
        default_value = saison._meta.get_field('nb_jours').default
        assert default_value == 23

    def test_object_verbose_name_plural(self):
        saison = Saison.objects.get(id='2020 - Septembre')
        verbose_name_plural = saison._meta.verbose_name_plural
        assert verbose_name_plural == "Périodes"

    def test_object_name_is_nom(self):
        saison = Saison.objects.get(id=1)
        expected_object_name = f'{saison.nom}'
        expected_object_name == str(saison.nom)
