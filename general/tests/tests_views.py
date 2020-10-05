from django.test import TestCase
from django.urls import reverse, reverse_lazy
import json
from django.contrib.auth.models import User
from general.models import Client, Commande, InfosTechniques, Forfait, Saison, Evenement


class ClientsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        test_user1.save()

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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/users/login/?next=%2F')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'general/home.html')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('')
        self.assertEqual(str(response.context['user']), 'testuser1')
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        assert response.status_code == 200

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))
        assert response.status_code == 200
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'general/home.html')

    def test_pagination_is_fiveteen(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue(len(response.context['clients']) == 50)

    def test_lists_all_clients(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        # Get second page and confirm it has (exactly) remaining 12 items
        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['clients']) == 13)

    def test_nb_clients_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('nb_clients' in response.context)
        self.assertTrue(response.context['nb_clients'] == 63)

    def test_total_commandes_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('total_commandes' in response.context)
        assert float(response.context['total_commandes']) == 391.00

    def test_nb_commandes_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('nb_commandes' in response.context)
        assert response.context['nb_commandes'] == 1

    def test_field_names_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('field_names' in response.context)
        assert response.context['field_names'] == ['Nom', 'Prenom', 'Téléphone', 'Commune']


class ClientsCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create_client'))
        self.assertRedirects(response, '/users/login/?next=/create/client')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/create/client')
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'general/create_client.html')

    def test_create_client(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
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
        self.assertEqual(Client.objects.last().id, 72)

    def test_create_client_and_command(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
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
        self.assertEqual(Client.objects.last().id, 73)
        self.assertEqual(Commande.objects.last().id, 5)
        self.assertEqual(Commande.objects.last().client.id, 72)

    def test_view_inlines_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200
        self.assertTrue('inlines' in response.context)

    def test_view_two_formset_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200
        formsets = [formset for formset in response.context['inlines']]
        self.assertTrue(len(formsets), 2)

    def test_view_form_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('create_client'))
        assert response.status_code == 200
        self.assertTrue('form' in response.context)


class ClientDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        Client.objects.create(
            prenom='TestDelete', nom='Jean', adresse='rue de paris',
            code_postal='33000', commune='Bordeaux', telephone='0787547810'
        )

    def test_redirect_if_not_logged_in(self):
        id_client = Client.objects.last().id
        response = self.client.get('/delete/{}'.format(id_client))
        self.assertRedirects(response, '/users/login/?next=/delete/{}'.format(id_client))

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(f'/delete/{Client.objects.get(prenom="TestDelete").id}', follow=True)
        assert response.status_code == 200

    def test_object_is_delete_with_post(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
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
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
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
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
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
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
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

    def test_redirect_if_not_logged_in(self):
        id_client = Client.objects.last().id
        response = self.client.get('/update/{}'.format(id_client))
        self.assertRedirects(response, '/users/login/?next=/update/{}'.format(id_client))

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(f'/update/{id_client_to_update}')
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'general/update_client.html')

    def test_update_client(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
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
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
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
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200
        self.assertTrue('inlines' in response.context)

    def test_view_two_formset_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200
        formsets = [formset for formset in response.context['inlines']]
        self.assertTrue(len(formsets), 3)

    def test_view_form_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        id_client_to_update = Client.objects.get(nom='Antoine').id
        response = self.client.get(reverse('update_client', kwargs={'pk': id_client_to_update}))
        assert response.status_code == 200
        self.assertTrue('form' in response.context)


class AjaxForfaitTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        saison = Saison.objects.create(nom='2020 - Octobre')
        Forfait.objects.create(nom='Forfait 2', description='Puissance inférieure à 18kVA', prix_ht=14.17,
                               taxe=20.00, prix_ttc=17.00, saison=saison)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/ajax_forfait/')
        self.assertRedirects(response, '/users/login/?next=/ajax_forfait/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/ajax_forfait/', {'forfait_name': ''})
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('ajax_forfait'), {'forfait_name': ''})
        assert response.status_code == 200

    def test_response_view_if_forfait_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        correct_response = json.dumps({"forfait_price_ht": '14.17', "forfait_price_ttc": '17.00',
                                       "forfait_taxe": '20.00'})
        response = self.client.get(reverse('ajax_forfait'), {'forfait_name': 'Forfait 2'})
        assert response.status_code == 200
        self.assertEqual(json.loads(response.content), json.loads(correct_response))

    def test_response_view_if_not_forfait_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        correct_response = json.dumps({"forfait_price_ht": 0.0, "forfait_price_ttc": 0.0,
                                       "forfait_taxe": 20.0})
        response = self.client.get(reverse('ajax_forfait'), {'forfait_name': ''})
        assert response.status_code == 200
        self.assertEqual(json.loads(response.content), json.loads(correct_response))


class ClientsSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        number_of_clients = 10

        for client_id in range(number_of_clients):
            Client.objects.create(
                prenom=f'Christian {client_id}',
                nom=f'Surname {client_id}',
                adresse=f' {client_id} rue de paris',
                code_postal=f'33000',
                commune='Bordeaux',
                telephone=f'07875478{client_id}',
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/ajax_search/client/')
        self.assertRedirects(response, '/users/login/?next=/ajax_search/client/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/ajax_search/client/', {'q': ''}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('ajax_search_client'), {'q': ''},
                                   **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        assert response.status_code == 200

    def test_response_view_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('ajax_search_client'), {'q': 'Surname 1'},
                                   **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'general/table_clients.html')

    def test_response_view_html_if_url_parameter(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('ajax_search_client'), {'q': 'Surname 1'},
                                   **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        assert response.status_code == 200
        self.assertContains(response, '<td>Surname 1</td>')

    def test_response_view_html_if_not_url_parameter(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('ajax_search_client'), {'q': ''},
                                   **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        assert response.status_code == 200
        for client in range(10):
            self.assertContains(response, f'<td>Surname {client}</td>')

    def test_response_view_html_ifrequest_is_not_ajax(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('ajax_search_client'), {'q': ''})
        assert response.status_code == 200
        for client in range(10):
            self.assertContains(response, f'<td>Surname {client}</td>')


class CommandesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        test_user1.save()
        client = Client.objects.create(nom='Rodriguez', prenom='Jean', adresse='13 rue de la paix', code_postal=75000,
                                       commune='Paris', telephone='0600112233', email='jean.villard@yahooo.com', )
        infos_techniques = InfosTechniques.objects.create(matricule_compteur='674', num_armoire='CH02')
        saison = Saison.objects.create(nom='2020 - Octobre')
        forfait = Forfait.objects.create(nom='Forfait 2', description='Puissance inférieure à 18kVA', prix_ht=14.17,
                                         taxe=20.00,
                                         prix_ttc=17.00, saison=saison)
        event = Evenement.objects.create(nom='Brocante des Quinquonces', ville='Bordeaux', type='Brocante')
        # Create 62 Clients for pagination tests
        number_of_commandes = 62

        for commande_id in range(number_of_commandes):
            Commande.objects.create(saison=saison, puissance=18, forfait=forfait, nb_jours=23, client=client,
                                    infos_techniques=infos_techniques,
                                    evenement=event, payee=True)




    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('commandes'))
        self.assertRedirects(response, '/users/login/?next=/commandes/')


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/commandes/')
        self.assertEqual(str(response.context['user']), 'testuser1')
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('commandes'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        assert response.status_code == 200

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('commandes'))
        assert response.status_code == 200
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'general/commandes_list.html')

    def test_pagination_is_fiveteen(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('commandes'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue(len(response.context['commandes']) == 50)

    def test_lists_all_commandes(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        # Get second page and confirm it has (exactly) remaining 12 items
        response = self.client.get(reverse('commandes') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['commandes']) == 12)

    def test_nb_commandes_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('commandes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('nb_commandes' in response.context)
        self.assertTrue(response.context['nb_commandes'] == 62)

    def test_total_commandes_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('commandes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('total_commandes_payee' in response.context)
        assert float(response.context['total_commandes_payee']) == 24242.00

    def test_nb_commandes_non_payee_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('commandes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('total_commandes_non_payee' in response.context)
        assert response.context['total_commandes_non_payee'] == None

    def test_field_names_in_context(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('commandes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('field_names' in response.context)
        assert response.context['field_names'] == ['Evènement', 'Saison', 'Client', 'Payée', 'Traitée par ACH', 'Date']
