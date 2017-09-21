from rest_framework import serializers
from labels.models import Label
import json

class LabelSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data['config'] = json.dumps(data.get('config'))
        return super(LabelSerializer, self).to_internal_value(data)


    def to_representation(self, obj):
        dat = super(LabelSerializer, self).to_representation(obj)
        dat['config'] = json.loads(dat.get('config', '{}'))
        del dat['project']
        del dat['dat']

        return dat

    class Meta:
        model = Label
        fields = ('id', 'config', 'project', 'dat')
