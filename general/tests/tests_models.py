from django.test import TestCase
from general.models import InfosTechniques
import pytest



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
