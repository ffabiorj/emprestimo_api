import uuid

from django.contrib.auth.models import User
from django.db import models


class Emprestimo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    valor_nominal = models.DecimalField(max_digits=7, decimal_places=2)
    taxa_juros = models.FloatField()
    endereco_ip = models.GenericIPAddressField()
    data_solicitacao = models.DateField()
    banco = models.CharField(max_length=150)
    cliente = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cliente: {self.owner} valor: R$ {str(self.valor_nominal)}"

    def saldo_devedor(self):
        pagamentos = sum(
            self.pagamentos.all().values_list("valor_pagamento", flat=True)
        )

        juros = (int(self.valor_nominal) * self.taxa_juros) / 100
        saldo_devedor = (float(self.valor_nominal) + juros) - float(pagamentos)

        return {"valor": saldo_devedor}


class Pagamento(models.Model):
    data_pagamento = models.DateField()
    valor_pagamento = models.DecimalField(max_digits=7, decimal_places=2)
    emprestimo = models.ForeignKey(
        Emprestimo, related_name="pagamentos", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.data_pagamento)
