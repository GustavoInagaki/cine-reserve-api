from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source='session.movie.title', read_only=True)
    session_time = serializers.DateTimeField(source='session.start_time', read_only=True)
    seat_code = serializers.CharField(source='seat.code', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'code',
            'created_at',
            'user',
            'session',
            'seat',
            'movie',
            'session_time',
            'seat_code',
        ]