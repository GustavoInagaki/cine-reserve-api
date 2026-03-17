from rest_framework.generics import ListAPIView
from .models import Movie, Session, Seat
from .serializers import MovieSerializer, SessionSerializer, SeatSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Seat
from datetime import timedelta
from django.utils import timezone
import uuid
from tickets.models import Ticket


class MovieListView(ListAPIView):
    queryset = Movie.objects.all().order_by('-release_date')
    serializer_class = MovieSerializer


class MovieSessionListView(ListAPIView):
    serializer_class = SessionSerializer

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Session.objects.filter(movie_id=movie_id).order_by('start_time')
    
class SessionSeatListView(ListAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        return Seat.objects.filter(session_id=session_id).order_by('code')
    
class SeatReserveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, seat_id):
        try:
            seat = Seat.objects.get(id=seat_id)
        except Seat.DoesNotExist:
            return Response({"error": "Seat not found"}, status=404)

        
        if seat.status == 'purchased':
            return Response({"error": "Seat already purchased"}, status=400)

       
        if seat.status == 'reserved':
            if seat.reserved_at:
                expiration_time = seat.reserved_at + timedelta(minutes=10)

                if timezone.now() > expiration_time:
                    
                    seat.status = 'available'
                    seat.reserved_at = None
                    seat.reserved_by = None
                else:
                    return Response({"error": "Seat still locked"}, status=400)

       
        seat.status = 'reserved'
        seat.reserved_at = timezone.now()
        seat.reserved_by = request.user
        seat.save()

        return Response({"message": "Seat reserved successfully"})
    

class SeatCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, seat_id):
        try:
            seat = Seat.objects.get(id=seat_id)
        except Seat.DoesNotExist:
            return Response({"error": "Seat not found"}, status=404)

        if seat.status == "available":
            return Response({"error": "Seat must be reserved first"}, status=400)

        if seat.status == "purchased":
            return Response({"error": "Seat already purchased"}, status=400)

        if seat.reserved_by != request.user:
            return Response({"error": "You can only checkout your own reservation"}, status=403)

        expiration_time = seat.reserved_at + timedelta(minutes=10)

        if timezone.now() > expiration_time:
            seat.status = "available"
            seat.reserved_at = None
            seat.reserved_by = None
            seat.save()
            return Response({"error": "Reservation expired"}, status=400)

        seat.status = "purchased"
        seat.save()

        ticket = Ticket.objects.create(
            user=request.user,
            session=seat.session,
            seat=seat,
            code=str(uuid.uuid4())[:8].upper()
        )

        return Response({
            "message": "Checkout completed successfully",
            "ticket_id": ticket.id,
            "ticket_code": ticket.code,
            "seat": seat.code,
            "session": seat.session.id,
            "movie": seat.session.movie.title
        }, status=201)