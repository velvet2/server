from rest_framework import serializers
from projects.models import Project
import json

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    def to_internal_value(self, data):
        data['config'] = json.dumps(data.get('config'))
        return super(ProjectSerializer, self).to_internal_value(data)


    def to_representation(self, obj):
        dat = super(ProjectSerializer, self).to_representation(obj)
        dat['config'] = json.loads(dat.get('config', '{}'))

        return dat

    class Meta:
        model = Project
        fields = ('id', 'name', 'dataset', 'owner', 'label', 'config')
