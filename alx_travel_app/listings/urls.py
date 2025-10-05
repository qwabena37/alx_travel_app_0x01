from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet

routers = DefaultRouter()

routers.register(r'listings', ListingViewSet, basename='listing')
routers.register(r'bookings', BookingViewSet, basename='booking')


urlpatterns = [
    path('', include(routers.urls)),
]
