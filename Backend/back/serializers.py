from .models import Match
from rest_framework import serializers

class MatchSerializer(serializers.ModelSerializer):

    date_played = serializers.DateTimeField(format='%d/%m/%Y', read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'username', 'date_played', 'who_win', 'game_type']
        extra_kwargs = {
            'user_name': {'required': True}
        }

    def create(self, validated_data):
        return Match.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('username', instance.user_id)
        instance.game_type = validated_data.get('game_type', instance.game_type)
        instance.who_win = validated_data.get('who_win', instance.who_win)
        instance.save()
        return instance