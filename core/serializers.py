from rest_framework import serializers
from core.models import Emprestimo, Pagamento


class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = (
            "id",
            "valor_nominal",
            "taxa_juros",
            "endereco_ip",
            "data_solicitacao",
            "banco",
            "cliente",
            "owner",
            "saldo_devedor",
        )


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        exclude = []
