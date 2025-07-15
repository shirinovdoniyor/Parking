



from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.views import register_api_view, login_api_view, profile_view, logout_api_view, parking_zone_list, \
    parking_zone_create, update_parking_zone, parking_spots_list, parking_spot_status, create_reservation, \
    list_reservations

urlpatterns = [
    path('register', register_api_view),
    path('login', login_api_view),
    path('profile/', profile_view),
    path('auth/logout/', logout_api_view, name='logout'),
    path('auth/parking_zones',parking_zone_list,name="parking_list"),
    path('api/parking-zones', parking_zone_create),
    path('api/parking-zones/<int:id>/', update_parking_zone, name='update_parking_zone'),
    path('api/spots/', parking_spots_list, name='parking_spots_list'),
    path('api/spots/<int:id>/status/', parking_spot_status, name='parking_spot_status'),
    path('api/reservations/', create_reservation, name='create_reservation'),
    path('api/reservations',list_reservations,name='list_reservation')
]


