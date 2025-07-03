from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserSerializer
from .permissions import IsModerator
from rest_framework import status
from rest_framework.response import Response
import logging

User = get_user_model()

class DeactivateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'User deactivated'}, status=status.HTTP_200_OK)

class ActivateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'User activated'}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class ManageUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

    def get_queryset(self):
        return User.objects.exclude(username='admin')

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger = logging.getLogger(__name__)
        logger.info(f"Data received: {request.data}")
        user = request.user
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({'error': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'status': 'Password updated successfully.'}, status=status.HTTP_200_OK)

class DeactivateSelfView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'status': 'Account deactivated'}, status=status.HTTP_200_OK)

class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsModerator]