from django.urls import path
from .views import MovieListView, MovieSessionListView, SessionSeatListView
from .views import SeatReserveView, SeatCheckoutView

urlpatterns = [
    path('', MovieListView.as_view(), name='movie-list'),
    path('<int:movie_id>/sessions/', MovieSessionListView.as_view(), name='movie-sessions'),
    path('sessions/<int:session_id>/seats/', SessionSeatListView.as_view(), name='session-seats'),
    path('seats/<int:seat_id>/reserve/', SeatReserveView.as_view()),
    path('seats/<int:seat_id>/checkout/', SeatCheckoutView.as_view()),
]