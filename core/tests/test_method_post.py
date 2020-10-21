import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APIClient
from django.test import TestCase
from core.models import Emprestimo


class PostEmprestimoTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        url = reverse("token")
        User.objects.create_user(username="teste", password="teste")
        data = {"username": "teste", "password": "teste"}
        token = self.client.post(url, data=data, follow=True)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])

    def test_post_status_code_201(self):
        data = {
            "valor_nominal": 10000.00,
            "taxa_juros": 10,
            "endereco_ip": "127.0.0.1",
            "data_solicitacao": "2020-10-10",
            "banco": "Santander",
            "cliente": "teste",
            "owner": 1,
        }

        result = self.client.post(
            reverse("emprestimos-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert result.status_code == HTTP_201_CREATED

    def test_post_status_code_401(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        data = {
            "valor_nominal": 10000.00,
            "taxa_juros": 10,
            "endereco_ip": "127.0.0.1",
            "data_solicitacao": "2020-10-10",
            "banco": "Santander",
            "cliente": "teste",
            "owner": 1,
        }
        result = self.client.post(
            reverse("emprestimos-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_post_status_code_400(self):
        data = {
            "valor_nominal": "afasfasfd",
            "taxa_juros": 10,
            "endereco_ip": "127.0.0.1",
            "data_solicitacao": 2020 - 10 - 10,
            "banco": "Santander",
            "cliente": "teste",
            "owner": 1,
        }
        result = self.client.post(
            reverse("emprestimos-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert result.status_code == HTTP_400_BAD_REQUEST


class PostPagamentoTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        url = reverse("token")
        owner = User.objects.create_user(username="teste", password="teste")
        data = {"username": "teste", "password": "teste"}
        token = self.client.post(url, data=data, follow=True)
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=10000,
            taxa_juros=10,
            endereco_ip="127.0.0.1",
            data_solicitacao="2020-12-10",
            banco="Santander",
            cliente="Petro",
            owner=owner,
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])

    def test_post_status_code_201(self):
        data = {
            "data_pagamento": "2020-12-10",
            "valor_pagamento": 100.00,
            "emprestimo": str(self.emprestimo.id),
        }

        result = self.client.post(
            reverse("pagamentos-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert result.status_code == HTTP_201_CREATED

    def test_post_status_code_401(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        data = {
            "data_pagamento": "2020-10-10",
            "valor_pagamento": 100,
            "emprestimo": str(self.emprestimo.id),
        }
        result = self.client.post(
            reverse("pagamentos-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_post_status_code_400(self):
        data = {
            "data_pagamento": 1,
            "valor_pagamento": "100",
            "emprestimo": str(self.emprestimo.id),
        }
        result = self.client.post(
            reverse("pagamentos-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert result.status_code == HTTP_400_BAD_REQUEST
