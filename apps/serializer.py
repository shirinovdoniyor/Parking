from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import User, ParkingZone, ParkingSpot, Reservation



class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username',"first_name","last_name", 'email', 'password'
        extra_kwargs = {'password': {'write_only': True}}
    def validate_password(self, value):
        return make_password(value)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate( username=username, password=password)

        if not user:
            raise serializers.ValidationError("Login yoki parol noto‘g‘ri yoki ro‘yxatdan o‘tmagan.")

        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_active', 'created_at')
        read_only_fields = ('email', 'role', 'is_active', 'created_at')



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate_refresh(self, value):
        if not value:
            raise serializers.ValidationError("Refresh token is required.")
        return value



class ParkingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingZone
        fields = [
            'id', 'name', 'address', 'coordinates',
            'total_spots', 'available_spots',
            'hourly_rate', 'daily_rate', 'monthly_rate',
            'created_at'
        ]
        read_only_fields = ['created_at']



class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = ['id', 'zone', 'spot_number', 'status', 'spot_type']




class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'spot', 'start_time', 'end_time', 'status', 'total_amount', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']