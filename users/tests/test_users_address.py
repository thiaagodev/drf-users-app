from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from validate_docbr import CPF
from users.models import User, Address


class AddressTestCase(APITestCase):
    def setUp(self):
        self.urls = reverse('address-list')

        cpf = CPF()
        user_cpf = cpf.generate()
        self.user = User.objects.create_user(email='teste@testcase.com', password='test123',
                                              first_name='Test', last_name='TestCase', cpf=user_cpf)
        Address.objects.create(id=1, owner=self.user, country='Brasil', state='SP', postal_code='18530-000', city='Tietê',
                               district='Loren ipsum', street='Loren ipsum ipsum', number=3)

    def test_create_address_without_authentication(self):
        """ Teste que verifica o que acontece se um usuário não autenticado
         tentar cadastrar um endereço """

        data = {
            "country": "Brasil",
            "state": "SP",
            "postal_code": "18530-000",
            "city": "Tietê",
            "district": "Loren ipsum",
            "street": "Loren ipsum ipsum",
            "number": 3
        }

        response = self.client.post(self.urls, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_address(self):
        """ Teste para criar um endereço apartir de um usuário autenticado """

        data = {
            "country": "Brasil",
            "state": "SP",
            "postal_code": "18530-000",
            "city": "Tietê",
            "district": "Loren ipsum",
            "street": "Loren ipsum ipsum",
            "number": 3
        }

        self.client.force_authenticate(self.user)
        response = self.client.post(self.urls, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_addresses_without_authentication(self):
        """ Teste que verifica o que acontece se um usuário não autenticado
         tentar visualizar todos os endereços """

        response = self.client.get(self.urls)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_addresses(self):
        """ Teste para visualizar todos os endereços de um usuário autenticado """

        self.client.force_authenticate(self.user)
        response = self.client.get(self.urls)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_address(self):
        """ Teste para atualizar um endereço de um usuário """

        data = {
            "country": "Brasil",
            "state": "RJ",
            "postal_code": "18530-000",
            "city": "Tietê",
            "district": "Loren ipsum",
            "street": "Loren ipsum ipsum",
            "number": 3
        }

        self.client.force_authenticate(self.user)
        response = self.client.put('/api/users/address/1/', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_one_address(self):
        """ Teste para deletar um endereço de um determinado usuário """

        self.client.force_authenticate(self.user)
        response = self.client.delete('/api/users/address/1/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
