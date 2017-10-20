from rest_framework import serializers

from comments_service.entity.models import Entity
from comments_service.entity.serializers import EntitySerializer
from .models import Comment

standard_fields_tuple = (
            'id',
            'entity',
            'to',
            'text'
        )


class CommentSerializer(serializers.ModelSerializer):
    entity = EntitySerializer()

    class Meta:
        model = Comment
        fields = standard_fields_tuple

    def create(self, validated_data):
        entity_data = validated_data.pop('entity')
        entity = Entity.objects.create(**entity_data)
        comment = Comment.objects.create(entity=entity, **validated_data)
        return comment

    def update(self, instance, validated_data):
        """
        Update and return an existing `Comment` instance, given the validated data.
        """
        entity_data = validated_data.pop('entity')
        for key, val in entity_data.items():
            setattr(instance.entity, key, val)
        instance.entity.save()
        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance


class CommentDeletedSerializer(serializers.ModelSerializer):
    entity = EntitySerializer()

    class Meta:
        model = Comment
        fields = standard_fields_tuple + ('is_deleted',)

