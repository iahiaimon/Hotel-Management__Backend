from django.urls import path
from .views import (
    RoomListView,
    RoomDetailView,
    ReviewListView,
    BookRoom
)

urlpatterns = [
    path("rooms/", RoomListView.as_view(), name="rooms"),
    path("rooms/<int:pk>/", RoomDetailView.as_view(), name="room-detail"),
    path("rooms/<int:room_id>/reviews/", ReviewListView.as_view(), name="room-reviews"),
    # path('rooms/<int:room_id>/reviews/<int:pk>/', ReviewDetailView.as_view(), name='room-review-detail'),
    path("rooms/<int:room_id>/book/", BookRoom, name="book_room"),
]
