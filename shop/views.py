from django.core.exceptions import ValidationError
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from users.permissions import IsModerator
from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer, OrderSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = cart_item.quantity + quantity if not created else quantity
        cart_item.save()
        return Response({'status': 'item added'})

    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        cart_item_id = request.data.get('cart_item_id')
        if not cart_item_id:
            return Response({'error': 'cart_item_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
            cart_item.delete()
            return Response({'status': 'item removed'})
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart.items.all():
            product = item.product
            if product.quantity_available < item.quantity:
                return Response(
                    {"detail": f"Product '{product.name}' non disponibile nella quantità richiesta. Quantità disponibile: {product.quantity_available}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()

        total = sum(
            item.product.get_discounted_price() * item.quantity
            for item in cart.items.all()
            if item.product.is_available()
        )

        order = serializer.save(user=user, amount=total)

        for item in cart.items.all():
            product = item.product
            product.quantity_available -= item.quantity
            product.save()

        cart.items.all().delete()

class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-id')

class ProductCreateUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator]

class OrderListAdminView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator]

class OrderUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        status_value = request.data.get('status')
        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status_value
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response({'status': 'Order deleted'}, status=status.HTTP_204_NO_CONTENT)