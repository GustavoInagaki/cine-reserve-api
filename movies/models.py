from django.db import models
from django.conf import settings


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField()  
    release_date = models.DateField()

    def __str__(self):
        return self.title
    
class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="sessions")
    start_time = models.DateTimeField()
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.movie.title} - {self.start_time}"
    
class Seat(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('purchased', 'Purchased'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='seats')
    code = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    reserved_at = models.DateTimeField(null=True, blank=True)
    reserved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ('session', 'code')

    def __str__(self):
        return f"{self.session} - {self.code} - {self.status}"