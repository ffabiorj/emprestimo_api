from core.viewsets import EmprestimoViewSet, PagamentoViewSet
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r"emprestimos", EmprestimoViewSet, basename="emprestimos")
router.register(r"pagamentos", PagamentoViewSet, basename="pagamentos")

urlpatterns = [
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("api/v1/", include(router.urls)),
]
