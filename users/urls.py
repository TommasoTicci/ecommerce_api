from django.urls import path
from .views import RegisterUserView, ProfileView, ManageUsersView, DeactivateUserView, ActivateUserView

urlpatterns = [
    # Registrazione nuovo utente
    path('register/', RegisterUserView.as_view(), name='user-register'),

    # Profilo utente autenticato (GET, PUT, PATCH)
    path('profile/', ProfileView.as_view(), name='user-profile'),

    # Lista utenti (solo moderatori)
    path('manage/', ManageUsersView.as_view(), name='user-manage'),

    # Disattivare utente (PATCH) — serve pk dell’utente
    path('<int:pk>/deactivate/', DeactivateUserView.as_view(), name='user-deactivate'),

    # Attivare utente (PATCH) — serve pk dell’utente
    path('<int:pk>/activate/', ActivateUserView.as_view(), name='user-activate'),
]