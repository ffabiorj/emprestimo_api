from core.models import Emprestimo, Pagamento
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient


class GetEmprestimoTest(TestCase):
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

    def test_metodo_get_status_code_200(self):
        result = self.client.get(reverse("emprestimos-list"))
        assert result.status_code == HTTP_200_OK

    def test_metodo_get_status_401(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.get(reverse("emprestimos-list"))
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_metodo_get_message_error(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.get(reverse("emprestimos-list"))
        expected = {"detail": "As credenciais de autenticação não foram fornecidas."}
        assert result.json() == expected

    def test_metodo_get_emprestimo_por_id(self):
        result = self.client.get(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)})
        )
        assert result.status_code == HTTP_200_OK

    def test_metodo_get_emprestimo_id_errado_erro_404(self):
        result = self.client.get(reverse("emprestimos-detail", kwargs={"pk": 30}))
        assert result.status_code == HTTP_404_NOT_FOUND

    def test_metodo_get_emprestimo_id_sem_autorizacao(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.get(
            reverse("emprestimos-detail", kwargs={"pk": str(self.emprestimo.id)})
        )
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_metodo_get_retorno_emprestimos_serializer(self):
        expect = [
            {
                "id": str(self.emprestimo.id),
                "valor_nominal": "10000.00",
                "taxa_juros": 10.0,
                "endereco_ip": "127.0.0.1",
                "data_solicitacao": "2020-10-10",
                "banco": "Santander",
                "cliente": "Petro",
                "owner": 1,
                "saldo_devedor": {"valor": 11000.0},
            }
        ]
        result = self.client.get(reverse("emprestimos-list"))
        assert result.json() == expect


class GetPagamentoTest(TestCase):
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

    def test_metodo_get_status_code_200(self):
        result = self.client.get(reverse("pagamentos-list"))
        assert result.status_code == HTTP_200_OK

    def test_metodo_get_status_401(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.get(reverse("pagamentos-list"))
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_metodo_get_message_error(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.get(reverse("pagamentos-list"))
        expected = {"detail": "As credenciais de autenticação não foram fornecidas."}
        assert result.json() == expected

    def test_metodo_get_pagamento_por_id(self):
        result = self.client.get(
            reverse("pagamentos-detail", kwargs={"pk": self.pagamento.id})
        )
        assert result.status_code == HTTP_200_OK

    def test_metodo_get_pagamento_id_errado(self):
        result = self.client.get(reverse("pagamentos-detail", kwargs={"pk": 30}))
        assert result.status_code == HTTP_404_NOT_FOUND

    def test_metodo_get_pagamento_id_sem_autorizacao(self):
        self.client = APIClient(HTTP_AUTHORIZATION="")
        result = self.client.get(
            reverse("pagamentos-detail", kwargs={"pk": self.pagamento.id})
        )
        assert result.status_code == HTTP_401_UNAUTHORIZED

    def test_metodo_get_retorno_pagamentos_serializer(self):
        expect = [
            {
                "id": 1,
                "data_pagamento": "2020-12-10",
                "valor_pagamento": "100.00",
                "emprestimo": str(self.emprestimo.id),
            }
        ]
        result = self.client.get(reverse("pagamentos-list"))
        assert result.json() == expect
