from rest_framework import serializers
from vote.models import *


class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = '__all__'
