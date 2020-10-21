import pytest
from core.models import Emprestimo, Pagamento
from django.contrib.auth.models import User


@pytest.fixture
def cria_user():
    return User.objects.create_user(username="fabio", password="12345678")


@pytest.fixture
def cria_emprestimo(cria_user):
    return Emprestimo.objects.create(
        valor_nominal=10000,
        taxa_juros=10,
        endereco_ip="127.0.0.1",
        data_solicitacao="2020-10-10",
        banco="Santander",
        cliente="Petro",
        owner=cria_user,
    )


@pytest.fixture
def cria_pagamento(cria_emprestimo):
    return Pagamento.objects.create(
        data_pagamento="2020-10-10", valor_pagamento=500.00, emprestimo=cria_emprestimo
    )


@pytest.mark.django_db
def test_cria_emprestimo(cria_emprestimo):
    assert Emprestimo.objects.count() == 1


@pytest.mark.django_db
def test_str_emprestimo(cria_emprestimo):
    assert cria_emprestimo.__str__() == "Cliente: fabio valor: R$ 10000"


@pytest.mark.django_db
def test_cria_pagamento(cria_pagamento):
    assert Pagamento.objects.count() == 1


@pytest.mark.django_db
def test_str_pagamento(cria_pagamento):
    assert cria_pagamento.__str__() == "2020-10-10"
