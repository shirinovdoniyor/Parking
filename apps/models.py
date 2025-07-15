
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


class User(AbstractUser):
    username = CharField(max_length=255,unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
        ('operator', 'Operator')
    ], default='user')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username




class ParkingZone(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    coordinates = models.CharField(max_length=100, help_text="Latitude,Longitude")
    total_spots = models.PositiveIntegerField(default=0)
    available_spots = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class ParkingSpot(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Maintenance'),
    ]

    SPOT_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('handicapped', 'Handicapped'),
        ('electric', 'Electric'),
    ]
    zone = models.ForeignKey(ParkingZone, related_name='spots', on_delete=models.CASCADE)
    spot_number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    spot_type = models.CharField(max_length=20, choices=SPOT_TYPE_CHOICES, default='regular')

    def __str__(self):
        return f"Spot {self.spot_number} ({self.get_spot_type_display()}) - {self.get_status_display()}"



class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation #{self.id} - Spot {self.spot.spot_number} - {self.status}"

