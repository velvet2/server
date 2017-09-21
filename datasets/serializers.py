from rest_framework import serializers
from datasets.models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dataset
        fields = ('id', 'name', 'owner')
