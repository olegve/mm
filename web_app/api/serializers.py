from rest_framework import serializers

from pydantic import BaseModel

from api.models import AbstractMessage


class AbstractMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractMessage
        # fields = (
        #     'message',
        #     'building',
        #     'system',
        #     'node',
        #     'priority',
        # )
        fields = '__all__'


class APIMessageSerializer(BaseModel):
    pass
