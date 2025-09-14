from django.shortcuts import render
from django.http import HttpResponse
from .models import Room, Review
from .serializers import RoomSerializer, ReviewSerializer
from django.contrib.auth import authenticate, login, logout


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes


class RoomListView(APIView):

    def get(self, request):
        rooms = Room.objects.filter(is_active=True)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailView(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_object(pk)
        if room is None:
            return Response(
                {"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        room = self.get_object(pk)
        if room is None:
            return Response(
                {"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room is None:
            return Response(
                {"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def BookRoom(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        if room.is_booked:
            return Response(
                {"detail": "Room already booked"}, status=status.HTTP_400_BAD_REQUEST
            )

        room.is_booked = True
        room.booked_by = request.user
        room.save()

        return Response(
            {"detail": f"Room booked successfully for {request.user.email}"}, status=200
        )

    except Room.DoesNotExist:
        return Response({"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(room_id=self.kwargs["room_id"])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, room_id=self.kwargs["room_id"])


# class ReviewDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, room_id, pk):
#         try:
#             return Review.objects.get(room_id=room_id, pk=pk)
#         except Review.DoesNotExist:
#             return None

#     def get(self, request, room_id, pk):
#         review = self.get_object(room_id, pk)
#         if review is None:
#             return Response(
#                 {"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = ReviewSerializer(review)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, room_id, pk):
#         review = self.get_object(room_id, pk)
#         if review is None:
#             return Response(
#                 {"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         if review.user != request.user:
#             return Response(
#                 {"error": "You do not have permission to edit this review."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )
#         serializer = ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, room_id, pk):
#         review = self.get_object(room_id, pk)
#         if review is None:
#             return Response(
#                 {"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         if review.user != request.user:
#             return Response(
#                 {"error": "You do not have permission to delete this review."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
