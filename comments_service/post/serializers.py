from comments_service.entity.serializers import EntitySerializer
from comments_service.entity_create_update_serializer import (
    EntityCreateUpdateSerializer)
from comments_service.post.models import Post


class PostSerializer(EntityCreateUpdateSerializer):
    entity = EntitySerializer()

    class Meta:
        model = Post
        fields = ('id',
                  'caption',
                  'entity')