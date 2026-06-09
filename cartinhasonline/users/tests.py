from django.test import TestCase
from users.models import CustomUser, CustomUserManager
from users.services import elo_calculation
from datetime import datetime, date
# Create your tests here.

class TestesCustomUser(TestCase):

    def setUp(self):
        self.strongPlayer = CustomUser.objects.create_user(
            email="teste@gmail.com",
            password = "123",
        )
        self.strongPlayer.elo = 1200
        self.strongPlayer.save()

        self.weakPlayer = CustomUser.objects.create_user(
            email="teste2@gmail.com",
            password = "233"
        )
        self.weakPlayer.elo = 500
        self.weakPlayer.save()

        self.adminAcc = CustomUser.objects.create_superuser(
            email="admin@gmail.com",
            password="666"
        )


    def test_match_results(self):
        strong_player_elo = self.strongPlayer.elo
        weak_player_elo = self.weakPlayer.elo

        newstrong_player_elo, newweak_player_elo = elo_calculation(strong_player_elo, weak_player_elo)

        self.assertTrue(newweak_player_elo < weak_player_elo)
        self.assertTrue(newstrong_player_elo > strong_player_elo)

    def test_is_super_user(self):
        self.assertTrue(self.adminAcc.is_superuser)
