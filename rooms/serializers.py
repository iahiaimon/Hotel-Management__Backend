from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError,
    StringRelatedField,
    EmailField,
)
from .models import Room, Review


class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = [
            "id",
            "title",
            "price",
            "image",
            "area",
            "beds",
            "baths",
            "guests",
            "description",
            "is_booked",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "is_active", "updated_at"]


class ReviewSerializer(ModelSerializer):
    # user_email = EmailField(source="user.email", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "room",
            "user",
            "rating",
            "comment",
            "is_active",
            "created_at",
            "updated_at",
        ]
        # extra_kwargs = {"user": {"write_only": True}}
        read_only_fields = [
            "id",
            "user",
            "room",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise ValidationError("Rating must be between 1 and 5.")
        return value
