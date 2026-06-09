from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from .services import create_match_and_update_elo
from .models import CustomUser, Match
from .serializers import UserSerializer, MatchSerializer

class RegisterUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CreateMatchView(CreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def perform_create(self, serializer):
        winner = serializer.validated_data['winner']
        loser = serializer.validated_data['loser']

        create_match_and_update_elo(winner, loser)
