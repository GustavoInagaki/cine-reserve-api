from rest_framework import serializers
from .models import Movie, Session, Seat


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'start_time', 'room', 'movie']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'