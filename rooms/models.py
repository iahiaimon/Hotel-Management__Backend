from django.db import models
from core.models.base_model import BaseModel
from accounts.models import CustomUser

# Create your models here.


class Room(BaseModel):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(max_length=500, null=True, blank=True)
    area = models.CharField(max_length=100)
    beds = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    description = models.TextField()
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )

    def __str__(self):
        return f"{self.id} -- {self.title}"


class Review(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.id} -- {self.room.title} -- {self.user.email}"
