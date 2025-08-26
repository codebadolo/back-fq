from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    UserListCreateView, UserUpdateView,
    PasswordResetRequestView, PasswordResetConfirmView , current_user
)

urlpatterns = [
    path('auth/signup/', RegisterView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/users/', UserListCreateView.as_view(), name='users-list'),
    path('auth/user/', current_user, name='current-user'),

    path('auth/users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('auth/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
