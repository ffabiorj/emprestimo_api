from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.models import Emprestimo, Pagamento

from .serializers import EmprestimoSerializer, PagamentoSerializer


class IsOwnerEmprestimo(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class IsOwnerPagamento(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.emprestimo.owner == request.user


class EmprestimoViewSet(ModelViewSet):
    """
    Uma simples view para visualizer, criar, atualizar e deletar um emprestimo.
    """

    permission_classes = [IsAuthenticated, IsOwnerEmprestimo]

    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer
    http_method_names = ["get", "post", "head", "put"]

    def get_queryset(self):
        user = self.request.user
        emprestimos = Emprestimo.objects.filter(owner=user)
        return emprestimos


class PagamentoViewSet(ModelViewSet):
    """
    Uma simples view para visualizer, criar, atualizar e deletar um pagamento.
    """

    permission_classes = [IsAuthenticated, IsOwnerPagamento]

    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    http_method_names = ["get", "post", "head", "put"]

    def get_queryset(self):
        user = self.request.user
        pagamentos = Pagamento.objects.filter(emprestimo__owner=user)
        return pagamentos
