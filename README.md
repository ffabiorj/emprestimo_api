[![Build Status](https://travis-ci.com/ffabiorj/emprestimo_api.svg?branch=master)](https://travis-ci.com/ffabiorj/voluntario_app)

[![codecov](https://codecov.io/gh/ffabiorj/emprestimo_api/branch/master/graph/badge.svg)](https://codecov.io/gh/ffabiorj/voluntario_app)

# Api de emprestimos

Criação de uma api de emprestimos

## Ferramentas utilizadas

- Django
- Django Rest FrameWork
- Postgres
- Docker

## Há duas maneiras de roda o projeto localmente:

### Sem docker.

1. Clone o repositório.
2. Entre na pasta.
3. Crie um ambiente de desenvolvimento com python 3.8.
4. Ative o ambiente.
5. Instale as dependências.
6. Crie um arquivo .env
7. Rode as migrações
8. Crie um usuário
9. Rode o projeto
10. Crie um token de acesso
11. Acesse o link

```
- git clone git@github.com:ffabiorj/emprestimo_api.git
- cd emprestimo_api
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements-dev.txt
- python contrib/env_gen.py
- python manage.py migrate
- python manage.py shell
  from django.contrib.auth.models import User
  user = User.objects.create_user(username=<yourname>', password='<password>')
  user.save()
- python manage.py runserver
- http://127.0.0.1:8000/api/v1/token/ username=<user> password=<password>
- http://127.0.0.1:8000/api/v1/emprestimos
```

### Com Docker e Docker Compose

1. Crie um arquivo .env
2. Crie um build do docker
3. Roda o docker Compose

```
- python contrib/env_gen.py
- docker-compose build
- docker-compose up
```

### Endpoints da api

- http://127.0.0.1:8000/api/v1/token/ # gera um token
- http://127.0.0.1:8000/api/v1/token/refresh/ # atualiza o token
- http://127.0.0.1:8000/api/v1/emprestimos/ # retorna todos os emprestimos do usuario
- http://127.0.0.1:8000/api/v1/emprestimos/id/ # retorna um emprestimo pelo id
- http://127.0.0.1:8000/api/v1/pagamentos/ # retorna todos os pagamentos do usuario
- http://127.0.0.1:8000/api/v1/pagamentos/id/ # retorna um pagamento pelo id

Obs.: Crie primeiro um emprestimo passando um id de um usuário valido.

- Exemplos de entrada para os endpoints

```
Dados para emprestimo
{
    "valor_nominal": 10000.00,
    "taxa_juros": 10,
    "endereco_ip": "127.0.0.1",
    "data_solicitacao": "2020-10-10",
    "banco": "Santander",
    "cliente": "teste",
    "owner": <id_user>
}

Dados para pagamento
{
    "data_pagamento": "2020-12-10",
    "valor_pagamento": 100.00,
    "emprestimo": <id_emprestimo>
}

Dados para gerar o token
{
    "usuario": <user>,
    "password": <password>
}

```

### Rodar os testes

```
pytest
```

### Links para as ferramentas utilizadas

[Django](https://docs.djangoproject.com/)

[Django Rest Framework](https://www.django-rest-framework.org/)

[Codecov](https://codecov.io/)

[Travis](https://travis-ci.com/)

[Postgres](https://www.postgresql.org/)

[Docker](https://www.docker.com/)
