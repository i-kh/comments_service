from rest_framework import serializers
from .models import CommentHistory


class CommentHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentHistory
        fields = ('id',
                  'date',
                  'changes',
                  'comment',
                  'type')
