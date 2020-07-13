from apps.sheet import models
from apps.media.api.serializers import MediaSerializer
from rest_framework import serializers


class CheatSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheatSheet
        fields = '__all__'
        extra_kwargs = {
            'slug': {'read_only': True},
            'user': {'read_only': True}
        }

    def to_representation(self, instance):
        self.fields['media'] = MediaSerializer(read_only=True)
        return super(CheatSheetSerializer, self).to_representation(instance)
