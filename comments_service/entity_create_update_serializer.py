from rest_framework import serializers

from comments_service.entity.models import Entity
from comments_service.entity.serializers import EntitySerializer


class EntityCreateUpdateSerializer(serializers.ModelSerializer):
    entity = EntitySerializer()

    def create(self, validated_data):
        """
        Create instance with corresponded Entity
        """
        entity_data = validated_data.pop('entity')
        entity = Entity.objects.create(**entity_data)
        comment = self.Meta.model.objects.create(entity=entity, **validated_data)
        return comment

    def update(self, instance, validated_data):
        """
        Update and return an existing instance.
        """
        entity_data = validated_data.pop('entity')
        for key, val in entity_data.items():
            setattr(instance.entity, key, val)
        instance.entity.save()
        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance