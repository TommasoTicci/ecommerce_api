from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductListView,
    ProductCreateUpdateDeleteView,
    CartViewSet,
    OrderCreateView,
    OrderListAdminView,
    UserOrderListView, OrderUpdateDeleteView,
)

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),

    path('products/<int:pk>/', ProductCreateUpdateDeleteView.as_view(), name='product-crud'),

    path('orders/', OrderCreateView.as_view(), name='order-create'),

    path('orders/admin/', OrderListAdminView.as_view(), name='admin-order-list'),

    path('orders/user/', UserOrderListView.as_view(), name='user-order-list'),

    path('orders/<int:pk>/', OrderUpdateDeleteView.as_view(), name='order-update-delete'),

    path('', include(router.urls)),
]