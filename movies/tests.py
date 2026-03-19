from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from users.models import User
from .models import Movie, Session, Seat
from tickets.models import Ticket


class SeatFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="gustavo",
            email="gustavo@email.com",
            password="12345678"
        )

        login_response = self.client.post("/api/users/login/", {
            "username": "gustavo",
            "password": "12345678"
        }, format="json")

        self.token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.movie = Movie.objects.create(
            title="Batman",
            description="Filme do Batman",
            duration=120,
            release_date="2024-01-10"
        )

        self.session = Session.objects.create(
            movie=self.movie,
            start_time=timezone.now(),
            room="Sala 1"
        )

        self.seat = Seat.objects.create(
            session=self.session,
            code="A1",
            status="available"
        )

    def test_reserve_seat(self):
        response = self.client.post(f"/api/movies/seats/{self.seat.id}/reserve/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.status, "reserved")
        self.assertEqual(self.seat.reserved_by, self.user)
        self.assertIsNotNone(self.seat.reserved_at)

    def test_checkout_seat(self):
        self.seat.status = "reserved"
        self.seat.reserved_at = timezone.now()
        self.seat.reserved_by = self.user
        self.seat.save()

        response = self.client.post(f"/api/movies/seats/{self.seat.id}/checkout/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.status, "purchased")
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.first().seat, self.seat)