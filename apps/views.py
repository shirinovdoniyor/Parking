from http import HTTPStatus
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404

from .models import ParkingZone, ParkingSpot, Reservation
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.serializer import UserModelSerializer, UserProfileSerializer, LoginSerializer, LogoutSerializer, \
    ParkingZoneSerializer, ParkingSpotSerializer, ReservationSerializer
from drf_spectacular.utils import extend_schema
from .admin import IsAdminOrReadOnly

# ------------------------AUTH-------------------------
@extend_schema(request=UserModelSerializer , responses=UserModelSerializer)
@extend_schema(tags=['auth'])
@api_view(['POST'])
def register_api_view(request):
    data = request.data
    serializer = UserModelSerializer(data=data)
    if serializer.is_valid():
        obj = serializer.save()
        return JsonResponse(UserModelSerializer(instance=obj).data)
    return Response(serializer.errors , status=HTTPStatus.BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses=LoginSerializer,
    tags=['auth']
)
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def login_api_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data, status=HTTP_200_OK)



@extend_schema(
    request=LogoutSerializer,
    responses={200: None},
    tags=["auth"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api_view(request):
    serializer = LogoutSerializer(data=request.data)
    if serializer.is_valid():
        try:
            token = RefreshToken(serializer.validated_data["refresh"])
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=200)
        except TokenError:
            return Response({"detail": "Invalid token."}, status=400)
    return Response(serializer.errors, status=400)


# ---------------------------------PARKING ZONE---------------------------------
@api_view(['GET'])
def parking_zone_list(request):
    zones = ParkingZone.objects.all()
    serializer = ParkingZoneSerializer(zones, many=True)
    return Response(serializer.data)

@extend_schema(
    request=ParkingZoneSerializer,
    responses=ParkingZoneSerializer,
    tags=["auth"]
)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def parking_zone_create(request):
    serializer = ParkingZoneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_parking_zone(request, id):
    zone = get_object_or_404(ParkingZone, id=id)
    serializer = ParkingZoneSerializer(zone, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------PARKING SPOTS-----------------------------------




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def parking_spots_list(request):
    spots = ParkingSpot.objects.all()
    serializer = ParkingSpotSerializer(spots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def parking_spot_status(request, id):
    spot = get_object_or_404(ParkingSpot, id=id)
    return Response({'id': spot.id, 'status': spot.status})






# -------------------------------RESERVATIONS--------------------------------------

@extend_schema(
    request=ReservationSerializer,
    responses=ReservationSerializer,
    tags=["auth"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        spot = serializer.validated_data['spot']
        if spot.status != 'available':
            return Response({'error': 'This spot is not available.'}, status=status.HTTP_400_BAD_REQUEST)

        spot.status = 'reserved'
        spot.save()

        reservation = serializer.save(user=request.user, status='active')
        return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=ReservationSerializer,
    responses=ReservationSerializer,
    tags=["auth"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)
