from core.models import Emprestimo, Pagamento
from django.contrib.auth.models import User
from django.test import TestCase


class EmprestimoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teste", password="teste")
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=10000,
            taxa_juros=10,
            endereco_ip="127.0.0.1",
            data_solicitacao="2020-10-10",
            banco="Santander",
            cliente="Petro",
            owner=self.user,
        )

    def teste_conta_um_emprestimo(self):
        assert Emprestimo.objects.count() == 1

    def test_verifica_str(self):
        assert self.emprestimo.__str__() == "Cliente: teste valor: R$ 10000"


class PagamentoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teste", password="teste")
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=10000,
            taxa_juros=10,
            endereco_ip="127.0.0.1",
            data_solicitacao="2020-10-10",
            banco="Santander",
            cliente="Petro",
            owner=self.user,
        )
        self.pagamento = Pagamento.objects.create(
            data_pagamento="2020-10-10",
            valor_pagamento=500.00,
            emprestimo=self.emprestimo,
        )

    def test_conta_um_pagamento(self):
        assert Pagamento.objects.count() == 1

    def test_verifica_str(self):
        assert self.pagamento.__str__() == "2020-10-10"
