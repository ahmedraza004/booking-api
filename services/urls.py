from django.urls import path, include   
from rest_framework.routers import DefaultRouter
from .views import CalendarBlockViewSet, ServiceViewSet, ServiceProviderViewSet, AvailabilityViewSet
router = DefaultRouter()

router.register(r'services', ServiceViewSet)
router.register(r'service-providers', ServiceProviderViewSet)
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'calendar-blocks', CalendarBlockViewSet) 

urlpatterns = [
    path('', include(router.urls)),
]
