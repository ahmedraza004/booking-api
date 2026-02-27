from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend

from .models import Booking, Payment, WeeklyAvailability, CalendarBlock
from .serializers import (
    BookingSerializer,
    PaymentSerializer,
    WeeklyAvailabilitySerializer,
    CalendarBlockSerializer,
)


# ----- Permissions ------------------------------------------------------------

class IsOwnerOrStaff(BasePermission):
    """
    Allow staff to access everything.
    For non-staff, restrict object-level access to their own Booking/Payment.
    """
    def has_object_permission(self, request, view, obj):
        if getattr(request.user, 'is_staff', False):
            return True
        # For Booking objects
        if hasattr(obj, 'user_id'):
            return obj.user_id == getattr(request.user, 'id', None)
        # For Payment objects: check related booking ownership
        if hasattr(obj, 'booking') and hasattr(obj.booking, 'user_id'):
            return obj.booking.user_id == getattr(request.user, 'id', None)
        return False


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


# ----- ViewSets ---------------------------------------------------------------

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['service_provider', 'service', 'status', 'date']
    ordering_fields = ['date', 'start_time', 'created_at']
    search_fields = ['service__name', 'service_provider__name']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs if getattr(user, 'is_staff', False) else qs.filter(user=user)

    def perform_create(self, serializer):
        # Bind booking to the authenticated user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if booking.status == Booking.CONFIRMED:
            return Response({'detail': 'Already confirmed.'}, status=status.HTTP_200_OK)

        # Re-run validation on current values (conflict checks in serializer.validate)
        ser = self.get_serializer(booking, data={}, partial=True)
        ser.is_valid(raise_exception=True)

        booking.status = Booking.CONFIRMED
        booking.save(update_fields=['status'])
        return Response({'detail': 'Booking confirmed.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status == Booking.CANCELED:
            return Response({'detail': 'Already canceled.'}, status=status.HTTP_200_OK)
        booking.status = Booking.CANCELED
        booking.save(update_fields=['status'])
        return Response({'detail': 'Booking canceled.'}, status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['payment_status', 'payment_method']
    ordering_fields = ['created_at', 'amount']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs if getattr(user, 'is_staff', False) else qs.filter(booking__user=user)

    @action(detail=True, methods=['post'])
    def capture(self, request, pk=None):
        """
        Stub capture endpoint.
        In real integration, talk to your PSP and set status accordingly.
        """
        payment = self.get_object()

        # Only owner or staff can capture (enforced by IsOwnerOrStaff)
        if payment.payment_status == Payment.STATUS_SUCCEEDED:
            return Response({'detail': 'Already captured.'}, status=status.HTTP_200_OK)

        if payment.booking.status != Booking.CONFIRMED:
            return Response({'detail': 'Booking must be confirmed before capture.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # TODO: integrate gateway here
        payment.payment_status = Payment.STATUS_SUCCEEDED
        payment.save(update_fields=['payment_status'])
        return Response({'detail': 'Payment captured.'}, status=status.HTTP_200_OK)


class WeeklyAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = WeeklyAvailability.objects.all()
    serializer_class = WeeklyAvailabilitySerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service_provider', 'day_of_week']
    ordering_fields = ['day_of_week', 'start_time']


class CalendarBlockViewSet(viewsets.ModelViewSet):
    queryset = CalendarBlock.objects.all()
    serializer_class = CalendarBlockSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service_provider', 'date']
    ordering_fields = ['date', 'start_time']