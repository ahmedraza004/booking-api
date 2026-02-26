# users/views.py
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserReadSerializer, UserWriteSerializer, SignupSerializer

User = get_user_model()

# ---- JWT Login with custom claims + is_active guard ----
class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if not user.is_active:
            # Prevent tokens for inactive users
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed("User account is inactive.")
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = getattr(user, 'role', None)
        return token

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class RefreshView(TokenRefreshView):
    pass

# ---- Signup ----
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

# ---- Profile (me) ----
class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserWriteSerializer
        return UserReadSerializer

# ---- Admin-only user list ----
from rest_framework.pagination import PageNumberPagination

class SmallPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserReadSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = SmallPagination