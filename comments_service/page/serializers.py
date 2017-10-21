from comments_service.entity.serializers import EntitySerializer
from comments_service.entity_create_update_serializer import (
    EntityCreateUpdateSerializer)
from comments_service.page.models import Page


class PageSerializer(EntityCreateUpdateSerializer):
    entity = EntitySerializer()

    class Meta:
        model = Page
        fields = ('id',
                  'caption',
                  'entity')
