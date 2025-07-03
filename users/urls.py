from django.urls import path
from .views import RegisterUserView, ProfileView, ManageUsersView, DeactivateUserView, ActivateUserView, \
    ChangePasswordView, DeactivateSelfView, DeleteUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='user-register'),

    path('profile/', ProfileView.as_view(), name='user-profile'),

    path('manage/', ManageUsersView.as_view(), name='user-manage'),

    path('<int:pk>/deactivate/', DeactivateUserView.as_view(), name='user-deactivate'),

    path('<int:pk>/activate/', ActivateUserView.as_view(), name='user-activate'),

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('deactivate/', DeactivateSelfView.as_view(), name='deactivate-self'),

    path('<int:pk>/delete/', DeleteUserView.as_view(), name='user-delete'),
]