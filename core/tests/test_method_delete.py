from core.models import Emprestimo, Pagamento
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import (
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient


class DeleteEmprestimoTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        url = reverse("token")
        self.owner = User.objects.create_user(
            username="teste",
            password="teste",
        )
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=10000,
            taxa_juros=10,
            endereco_ip="127.0.0.1",
            data_solicitacao="2020-10-10",
            banco="Santander",
            cliente="Petro",
            owner=self.owner,
        )
        data = {"username": "teste", "password": "teste"}
        token = self.client.post(url, data=data, follow=True)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])

    def test_delete_status_code_405(self):
        result = self.client.delete(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)})
        )
        assert result.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_status_401(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.delete(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)})
        )
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_delete_message_error(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.delete(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)})
        )
        expected = {"detail": "As credenciais de autenticação não foram fornecidas."}
        assert result.json() == expected

    def test_delete_emprestimo_id_errado_erro_404(self):
        result = self.client.delete(reverse("emprestimos-detail", kwargs={"pk": 5}))
        assert result.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_emprestimo_id_message_erro(self):
        result = self.client.delete(reverse("emprestimos-detail", kwargs={"pk": 5}))
        print(result.json())
        expected = {"detail": 'Método "DELETE" não é permitido.'}
        assert result.json() == expected


class DeletePagamentoTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        url = reverse("token")
        self.owner = User.objects.create_user(
            username="teste",
            password="teste",
        )
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=10000,
            taxa_juros=10,
            endereco_ip="127.0.0.1",
            data_solicitacao="2020-10-10",
            banco="Santander",
            cliente="Petro",
            owner=self.owner,
        )
        self.pagamento = Pagamento.objects.create(
            data_pagamento="2020-12-10",
            valor_pagamento=100.00,
            emprestimo=self.emprestimo,
        )
        data = {"username": "teste", "password": "teste"}
        token = self.client.post(url, data=data, follow=True)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])

    def test_delete_status_code_204(self):
        result = self.client.delete(
            reverse("pagamentos-detail", kwargs={"pk": self.pagamento.id})
        )
        assert result.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_status_401(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.delete(
            reverse("pagamentos-detail", kwargs={"pk": self.pagamento.id})
        )
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_delete_message_error(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.delete(
            reverse("pagamentos-detail", kwargs={"pk": self.pagamento.id})
        )
        expected = {"detail": "As credenciais de autenticação não foram fornecidas."}
        assert result.json() == expected

    def test_delete_pagamento_id_errado(self):
        result = self.client.delete(reverse("pagamentos-detail", kwargs={"pk": 30}))
        assert result.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_emprestimo_id_message_erro(self):
        result = self.client.delete(reverse("emprestimos-detail", kwargs={"pk": 5}))
        expected = {"detail": 'Método "DELETE" não é permitido.'}
        assert result.json() == expected