from rest_framework import serializers
from datas.models import Data

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('id', 'name', 'path', 'datatype')
