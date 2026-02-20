# users/urls.py
from django.urls import path
from .views import SignupView, LoginView, RefreshView, MeView, UserListView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('list/', UserListView.as_view(), name='users_list'),  # admin only (optional)
]   