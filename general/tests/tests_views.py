from django.test import TestCase
from django.urls import reverse, reverse_lazy
from general.models import Client, Commande, InfosTechniques, Forfait, Saison, Evenement


class ClientsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 62 Clients for pagination tests
        number_of_clients = 62

        for client_id in range(number_of_clients):
            Client.objects.create(
                prenom=f'Christian {client_id}',
                nom=f'Surname {client_id}',
                adresse=f' {client_id} rue de paris',
                code_postal=f'33000',
                commune='Bordeaux',
                telephone=f'07875478{client_id}',
            )
        infos_techniques = InfosTechniques.objects.create(matricule_compteur='674', num_armoire='CH02')
        saison = Saison.objects.create(nom='2020 - Octobre')
        forfait = Forfait.objects.create(nom='Forfait 2', description='Puissance inférieure à 18kVA', prix_ht=14.17,
                                         taxe=20.00,
                                         prix_ttc=17.00, saison=saison)
        client = Client.objects.create(nom='Rodriguez', prenom='Jean', adresse='13 rue de la paix', code_postal=75000,
                                       commune='Paris', telephone='0600112233', email='jean.villard@yahooo.com', )
        event = Evenement.objects.create(nom='Brocante des Quinquonces', ville='Bordeaux', type='Brocante')
        Commande.objects.create(saison=saison, puissance=18, forfait=forfait, nb_jours=23, client=client,
                                infos_techniques=infos_techniques,
                                evenement=event, payee=True)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        assert response.status_code == 200

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'general/home.html')

    def test_pagination_is_fiveteen(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['clients']) == 50)

    def test_lists_all_clients(self):
        # Get second page and confirm it has (exactly) remaining 12 items
        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['clients']) == 13)

    def test_nb_clients_in_context(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('nb_clients' in response.context)
        self.assertTrue(response.context['nb_clients'] == 63)

    def test_total_commandes_in_context(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('total_commandes' in response.context)
        assert float(response.context['total_commandes']) == 391.09

    def test_nb_commandes_in_context(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('nb_commandes' in response.context)
        assert response.context['nb_commandes'] == 1

    def test_field_names_in_context(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('field_names' in response.context)
        assert response.context['field_names'] == ['Nom', 'Prenom', 'Téléphone', 'Commune']


class ClientsCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(
            prenom='Christian', nom='Surname', adresse='rue de paris',
            code_postal='33000', commune='Bordeaux', telephone='0787547810'
        )
        InfosTechniques.objects.create(matricule_compteur='674', num_armoire='CH02')
        saison = Saison.objects.create(nom='2020 - Octobre')
        Forfait.objects.create(nom='Forfait 2', description='Puissance inférieure à 18kVA', prix_ht=14.17,
                               taxe=20.00,
                               prix_ttc=17.00, saison=saison)
        Evenement.objects.create(nom='Brocante des Quinquonces', ville='Bordeaux', type='Brocante')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/create/client')
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'general/create_client.html')

    def test_create_client(self):
        data = {}
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200

        formsets = [formset for formset in response.context['inlines']]
        for formset in formsets:
            for field in formset.management_form:
                data["-".join((formset.management_form.prefix, field.name))] = field.value()
            for form in formset:
                for field in form:
                    data["-".join((form.prefix, field.name))] = field.value() if field.value() is not None else ''
        client = {'prenom': 'ChriTest', 'nom': 'Test', 'adresse': 'rue de paris',
                  'code_postal': '33000', 'commune': 'Bordeaux', 'telephone': '0787547810'}
        for key, value in client.items():
            data[key] = value

        self.client.post(reverse('create_client'), data)
        self.assertEqual(Client.objects.last().id, 71)

    def test_create_client_and_command(self):
        data = {}
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200

        formsets = [formset for formset in response.context['inlines']]
        for formset in formsets:
            for field in formset.management_form:
                data["-".join((formset.management_form.prefix, field.name))] = field.value()

        client = {'prenom': 'ChriTest', 'nom': 'Test2', 'adresse': 'rue de paris',
                  'code_postal': '33000', 'commune': 'Bordeaux', 'telephone': '0787547810'}
        commande = {'client-0-saison': Saison.objects.last().nom, 'client-0-evenement': Evenement.objects.last().id,
                    'client-0-puissance': 18,
                    'client-0-forfait': Forfait.objects.last().nom,
                    'client-0-nb_jours': 23, 'client-0-client': '',
                    'client-0-infos_techniques': InfosTechniques.objects.last().id,
                    'client-0-total_ht': 0.0, 'client-0-total_ttc': 0.0, 'client-0-payee': False,
                    'client-0-id': '',
                    'client-1-saison': '', 'client-1-evenement': '', 'client-1-puissance': 0,
                    'client-1-forfait': '',
                    'client-1-nb_jours': 23, 'client-1-client': '', 'client-1-infos_techniques': '',
                    'client-1-total_ht': 0.0, 'client-1-total_ttc': 0.0, 'client-1-payee': False,
                    'client-1-id': ''}
        for key, value in client.items():
            data[key] = value
        for key, value in commande.items():
            data[key] = value

        self.client.post(reverse('create_client'), data)
        self.assertEqual(Client.objects.last().id, 72)
        self.assertEqual(Commande.objects.last().id, 4)
        self.assertEqual(Commande.objects.last().client.id, 72)

    def test_view_inlines_in_context(self):
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200
        self.assertTrue('inlines' in response.context)

    def test_view_two_formset_in_context(self):
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200
        formsets = [formset for formset in response.context['inlines']]
        self.assertTrue(len(formsets), 2)

    def test_view_form_in_context(self):
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200
        self.assertTrue('form' in response.context)


class ClientDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(
            prenom='TestDelete', nom='Jean', adresse='rue de paris',
            code_postal='33000', commune='Bordeaux', telephone='0787547810'
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/delete/{Client.objects.get(prenom="TestDelete").id}', follow=True)
        assert response.status_code == 200

    def test_object_is_delete_with_post(self):
        Client.objects.create(
            prenom='TestDelete2', nom='Jean', adresse='rue de paris',
            code_postal='33000', commune='Bordeaux', telephone='0787547810'
        )
        id_client = Client.objects.get(prenom="TestDelete2").id
        self.client.post(f'/delete/{id_client}')

        # verifies that a non-existent object returns a 404 error.
        null_response = self.client.get(f'/delete/{id_client}')
        self.assertEqual(null_response.status_code, 404)

    def test_object_is_delete_with_get(self):
        Client.objects.create(
            prenom='TestDelete3', nom='Jean', adresse='rue de paris',
            code_postal='33000', commune='Bordeaux', telephone='0787547810'
        )
        id_client = Client.objects.get(prenom="TestDelete3").id
        self.client.get(f'/delete/{id_client}')

        # verifies that a non-existent object returns a 404 error.
        null_response = self.client.get(f'/delete/{id_client}')
        self.assertEqual(null_response.status_code, 404)

    def test_success_redirect_after_delete(self):
        Client.objects.create(
            prenom='TestDelete4', nom='Jean', adresse='rue de paris',
            code_postal='33000', commune='Bordeaux', telephone='0787547810'
        )
        id_client = Client.objects.get(prenom="TestDelete4").id
        success_url = reverse_lazy('home')
        response = self.client.get(f'/delete/{id_client}', follow=True)
        self.assertRedirects(response, success_url)


class UpdateClientViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = Client.objects.create(
            prenom='Michel', nom='Antoine', adresse='rue de paris',
            code_postal='33000', commune='Bordeaux', telephone='0787547810'
        )
        infos_techniques = InfosTechniques.objects.create(matricule_compteur='670', num_armoire='CH02')
        saison = Saison.objects.create(nom='2020 - Octobre')
        forfait = Forfait.objects.create(nom='Forfait 2', description='Puissance inférieure à 18kVA', prix_ht=14.17,
                                         taxe=20.00,
                                         prix_ttc=17.00, saison=saison)
        event = Evenement.objects.create(nom='Brocante des Quinquonces', ville='Bordeaux', type='Brocante')
        Commande.objects.create(saison=saison, puissance=20, forfait=forfait, nb_jours=23, client=client,
                                infos_techniques=infos_techniques,
                                evenement=event, payee=True)

    def test_view_url_exists_at_desired_location(self):
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(f'/update/{id_client_to_update}')
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200

    def test_view_uses_correct_template(self):
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'general/update_client.html')

    def test_update_client(self):
        id_client_to_update = Client.objects.get(nom='Antoine').id
        data = {}
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200

        formsets = [formset for formset in response.context['inlines']]
        for formset in formsets:
            for field in formset.management_form:
                data["-".join((formset.management_form.prefix, field.name))] = field.value()
            for form in formset:
                for field in form:
                    data["-".join((form.prefix, field.name))] = field.value() if field.value() is not None else ''
        client = {'prenom': 'Marc', 'nom': 'Antoine', 'adresse': 'rue de paris',
                  'code_postal': '33000', 'commune': 'Bordeaux', 'telephone': '0787547810'}
        for key, value in client.items():
            data[key] = value

        self.client.post(reverse('update_client', kwargs={'pk': id_client_to_update}), data, follow=True)
        self.assertEqual(Client.objects.last().prenom, 'Marc')

    def test_update_client_and_command(self):
        id_client_to_update = Client.objects.get(nom='Antoine').id
        data = {}
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200

        formsets = [formset for formset in response.context['inlines']]
        for formset in formsets:
            for field in formset.management_form:
                data["-".join((formset.management_form.prefix, field.name))] = field.value()

        client = {'prenom': 'Paul', 'nom': 'Antoine', 'adresse': 'rue de paris',
                  'code_postal': '33000', 'commune': 'Bordeaux', 'telephone': '0787547810'}
        commande = {'client-0-saison': Saison.objects.last().nom, 'client-0-evenement': Evenement.objects.last().id,
                    'client-0-puissance': 24,
                    'client-0-forfait': Forfait.objects.last().nom,
                    'client-0-nb_jours': 23, 'client-0-client': id_client_to_update,
                    'client-0-infos_techniques': InfosTechniques.objects.last().id,
                    'client-0-total_ht': 0.0, 'client-0-total_ttc': 0.0, 'client-0-payee': True,
                    'client-0-id': Commande.objects.last().id,
                    'client-1-saison': '', 'client-1-evenement': '', 'client-1-puissance': 0,
                    'client-1-forfait': '',
                    'client-1-nb_jours': 23, 'client-1-client': '', 'client-1-infos_techniques': '',
                    'client-1-total_ht': 0.0, 'client-1-total_ttc': 0.0, 'client-1-payee': False,
                    'client-1-id': '',
                    'client-2-saison': '', 'client-2-evenement': '', 'client-2-puissance': 0,
                    'client-2-forfait': '',
                    'client-2-nb_jours': 23, 'client-2-client': '', 'client-2-infos_techniques': '',
                    'client-2-total_ht': 0.0, 'client-2-total_ttc': 0.0, 'client-2-payee': False,
                    'client-2-id': ''
                    }
        for key, value in client.items():
            data[key] = value
        for key, value in commande.items():
            data[key] = value
        self.client.post(reverse('update_client', kwargs={'pk': id_client_to_update}), data)
        self.assertEqual(Commande.objects.last().puissance, 24)
        self.assertEqual(Commande.objects.last().client.prenom, 'Paul')

    def test_view_inlines_in_context(self):
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200
        self.assertTrue('inlines' in response.context)

    def test_view_two_formset_in_context(self):
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200
        formsets = [formset for formset in response.context['inlines']]
        self.assertTrue(len(formsets), 3)

    def test_view_form_in_context(self):
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200
        self.assertTrue('form' in response.context)

class AjaxForfaitTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass