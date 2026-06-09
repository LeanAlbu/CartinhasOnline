from django.db import transaction
from .models import Match

def elo_calculation(winner_elo: int, loser_elo: int) -> tuple[int, int]:

    #for the winner
    expected_score_win = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    new_winner = round(winner_elo + 32 * (1 - expected_score_win))

    #for the loser

    expected_score_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))
    new_loser = round(loser_elo + 32 * (0 - expected_score_loser))

    return new_winner, new_loser

@transaction.atomic
def create_match_and_update_elo(winner, loser):
    new_winner_elo, new_loser_elo = elo_calculation(winner.elo, loser.elo)

    winner.elo = new_winner_elo
    winner.save()

    loser.elo = new_loser_elo
    loser.save()

    match = Match.objects.create(winner=winner, loser=loser)
    return match
