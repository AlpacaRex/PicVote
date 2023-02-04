from rest_framework import serializers
from vote.models import *


class VotingItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = VotingItem
        fields = '__all__'


class VotingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = ('id', 'title', 'date_created')


class VotingSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%Y-%m-%d, %H:%M:%S", required=False)
    items = VotingItemSerializer(many=True, required=False)

    class Meta:
        model = Voting
        fields = '__all__'



