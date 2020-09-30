from rest_framework import serializers


class TestSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=20, required=True)
    code = serializers.CharField(max_length=20, required=True)