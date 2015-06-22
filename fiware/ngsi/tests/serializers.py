from rest_framework import serializers
from fiware.ngsi.tests.models import TestModel


class TestModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestModel
