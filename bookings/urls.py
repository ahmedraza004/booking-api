from django.urls import path, include
from rest_framework.routers import DefaultRouter    
from .views import BookingViewSet, PaymentViewSet, WeeklyAvailabilityViewSet, CalendarBlockViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'weekly-availabilities', WeeklyAvailabilityViewSet)
router.register(r'calendar-blocks', CalendarBlockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]