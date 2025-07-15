from django.contrib import admin
from apps.models import User, ParkingZone, ParkingSpot
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rest_framework import permissions


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff





@admin.register(ParkingZone)
class ParkingZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'total_spots', 'available_spots', 'hourly_rate')
    search_fields = ('name', 'address')
    list_filter = ('name',)
    ordering = ('id',)




@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('id', 'zone', 'spot_number', 'status', 'spot_type')
    list_filter = ('status', 'spot_type', 'zone')
    search_fields = ('spot_number',)