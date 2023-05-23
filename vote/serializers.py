import time

from rest_framework import serializers
from vote.models import *


class VotingItemSerializer(serializers.ModelSerializer):
    num = serializers.IntegerField(required=False)

    class Meta:
        model = VotingItem
        fields = '__all__'


class VotingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = ('id', 'title', 'date_created')


class VotingSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(required=False)
    deadline = serializers.DateTimeField(required=False)
    items = VotingItemSerializer(many=True, required=False)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Voting
        exclude = ('history',)



