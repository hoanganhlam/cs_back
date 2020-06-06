from apps.sheet import models
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
        return super(CheatSheetSerializer, self).to_representation(instance)
