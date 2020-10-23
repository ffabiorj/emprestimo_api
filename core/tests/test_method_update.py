import json

from core.models import Emprestimo, Pagamento
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APIClient


class UpdateEmprestimoTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client2 = APIClient()

        url = reverse("token")
        self.owner = User.objects.create_user(
            username="teste",
            password="teste",
        )
        User.objects.create_user(
            username="teste2",
            password="teste2",
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
        self.payload_emprestimo_correto = {
            "valor_nominal": 20000,
            "taxa_juros": 5.0,
            "endereco_ip": "127.0.0.20",
            "data_solicitacao": "2020-10-10",
            "banco": "Santander",
            "cliente": "Petro",
            "owner": 1,
        }
        self.payload_emprestimo_errado = {
            "valor_nominal": "20000",
            "taxa_juros": "5.0",
            "endereco_ip": "127.0.0.20",
            "data_solicitacao": "2020-10-10",
            "banco": "",
            "cliente": "",
            "owner": 1,
        }
        data = {"username": "teste", "password": "teste"}
        data2 = {"username": "teste2", "password": "teste2"}

        token = self.client.post(url, data=data, follow=True)
        token2 = self.client.post(url, data=data2, follow=True)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])
        self.client2.credentials(HTTP_AUTHORIZATION="Bearer " + token2.data["access"])

    def test_metodo_update_status_code_200(self):
        result = self.client.put(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)}),
            data=json.dumps(self.payload_emprestimo_correto),
            content_type="application/json",
        )
        assert result.status_code == HTTP_200_OK

    def test_metodo_update_status_code_400(self):
        result = self.client.put(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)}),
            data=json.dumps(self.payload_emprestimo_errado),
            content_type="application/json",
        )
        assert result.status_code == HTTP_400_BAD_REQUEST

    def test_metodo_update_status_401(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.put(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)}),
            data=json.dumps(self.payload_emprestimo_correto),
            content_type="application/json",
        )
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_metodo_update_message_error(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.put(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)}),
            data=json.dumps(self.payload_emprestimo_correto),
            content_type="application/json",
        )
        expected = {"detail": "As credenciais de autenticação não foram fornecidas."}
        assert result.json() == expected

    def test_updete_emprestimo_id_errado_erro_404(self):
        result = self.client.put(
            reverse("emprestimos-detail", kwargs={"pk": 5}),
            data=json.dumps(self.payload_emprestimo_correto),
            content_type="application/json",
        )
        assert result.status_code == HTTP_404_NOT_FOUND

    def test_metodo_nao_permiti_update_emprestimo_outro_usuario(self):
        result = self.client2.put(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)}),
            data=json.dumps(self.payload_emprestimo_correto),
            content_type="application/json",
        )
        assert result.status_code == HTTP_404_NOT_FOUND


class GetPagamentoTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client2 = APIClient()

        url = reverse("token")
        self.owner = User.objects.create_user(
            username="teste",
            password="teste",
        )
        User.objects.create_user(
            username="teste2",
            password="teste2",
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
        self.payload_pagamento_correto = {
            "data_pagamento": "2020-12-25",
            "valor_pagamento": 150.00,
            "emprestimo": str(self.emprestimo.id),
        }
        self.payload_pagamento_errado = {
            "data_pagamento": 10,
            "valor_pagamento": "",
            "emprestimo": str(self.emprestimo.id),
        }
        data = {"username": "teste", "password": "teste"}
        data2 = {"username": "teste2", "password": "teste2"}

        token = self.client.post(url, data=data, follow=True)
        token2 = self.client.post(url, data=data2, follow=True)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])
        self.client2.credentials(HTTP_AUTHORIZATION="Bearer " + token2.data["access"])

    def test_metodo_update_status_code_200(self):
        result = self.client.put(
            reverse("pagamentos-detail", kwargs={"pk": self.pagamento.id}),
            data=json.dumps(self.payload_pagamento_correto),
            content_type="application/json",
        )
        assert result.status_code == HTTP_200_OK

    def test_metodo_update_status_code_400(self):
        result = self.client.put(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)}),
            data=json.dumps(self.payload_pagamento_errado),
            content_type="application/json",
        )
        assert result.status_code == HTTP_400_BAD_REQUEST

    def test_metodo_update_status_401(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.put(
            reverse("pagamentos-detail", kwargs={"pk": self.pagamento.id}),
            data=json.dumps(self.payload_pagamento_correto),
            content_type="application/json",
        )
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_metodo_update_message_error(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.put(
            reverse("pagamentos-detail", kwargs={"pk": self.pagamento.id}),
            data=json.dumps(self.payload_pagamento_correto),
            content_type="application/json",
        )
        expected = {"detail": "As credenciais de autenticação não foram fornecidas."}
        assert result.json() == expected

    def test_metodo_update_pagamento_id_errado(self):
        result = self.client.put(
            reverse("pagamentos-detail", kwargs={"pk": 30}),
            data=json.dumps(self.payload_pagamento_correto),
            content_type="application/json",
        )
        assert result.status_code == HTTP_404_NOT_FOUND

    def test_metodo_nao_permite_update_pagamento_outro_usuario(self):
        result = self.client2.put(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)}),
            data=json.dumps(self.payload_pagamento_correto),
            content_type="application/json",
        )
        assert result.status_code == HTTP_404_NOT_FOUND
