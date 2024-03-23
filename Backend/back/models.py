from django.db import models

class Match(models.Model):
    username = models.CharField(max_length=255)
    date_played = models.DateTimeField(auto_now_add=True)
    who_win = models.CharField(blank=False)
    game_type = models.CharField(max_length=255)
