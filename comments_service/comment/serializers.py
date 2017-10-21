from rest_framework import serializers

from comments_service.entity.models import Entity
from comments_service.entity.serializers import EntitySerializer
from comments_service.entity_create_update_serializer import (
    EntityCreateUpdateSerializer)
from .models import Comment

standard_fields_tuple = (
            'id',
            'entity',
            'to',
            'text'
        )


class CommentSerializer(EntityCreateUpdateSerializer):
    entity = EntitySerializer()

    class Meta:
        model = Comment
        fields = standard_fields_tuple


class CommentDeletedSerializer(serializers.ModelSerializer):
    entity = EntitySerializer()

    class Meta:
        model = Comment
        fields = standard_fields_tuple + ('is_deleted',)

