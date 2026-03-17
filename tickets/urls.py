from django.urls import path
from .views import UserTicketListView

urlpatterns = [
    path('my-tickets/', UserTicketListView.as_view()),
]