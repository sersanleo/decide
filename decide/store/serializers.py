from rest_framework import serializers

from .models import Vote


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()
    c = serializers.IntegerField()
    d = serializers.IntegerField()

    class Meta:
        model = Vote
        fields = ('voting_id', 'voter_id','question_id','sex', 'a', 'b')

