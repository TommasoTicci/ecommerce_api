from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductListView,
    ProductCreateUpdateDeleteView,
    CartViewSet,
    OrderCreateView,
    OrderListAdminView,
)

# Router per CartViewSet
router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    # ✅ Lista prodotti (GET per tutti)
    path('products/', ProductListView.as_view(), name='product-list'),

    # ✅ CRUD prodotti per moderatori (POST, GET, PUT/PATCH, DELETE su singolo prodotto)
    path('products/<int:pk>/', ProductCreateUpdateDeleteView.as_view(), name='product-crud'),

    # ✅ Creazione ordine (POST per utenti autenticati)
    path('orders/', OrderCreateView.as_view(), name='order-create'),

    # ✅ Visualizzazione ordini per moderatori
    path('orders/admin/', OrderListAdminView.as_view(), name='admin-order-list'),

    # ✅ CartViewSet gestito via router (CRUD carrello + add_item)
    path('', include(router.urls)),
]