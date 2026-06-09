from rest_framework import serializers
from .models import CustomUser, Match

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'elo']
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def create(self, validated_data):
        newUser = CustomUser.objects.create_user(**validated_data)
        return newUser

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['winner', 'loser', 'match_date']
        read_only_fields = ['id', 'created_at']
