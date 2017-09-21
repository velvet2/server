from projects.models import Project
from datas.models import Data
from labels.models import Label
from labels.serializers import LabelSerializer
from datas.serializers import DataSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from server import settings
import json
import base64
from datasets import expression

class LabelList(APIView):
    def get(self, request, format=None):
        project_id = request.GET.get('project')
        if project_id is None:
            return Response({"error": "project parameter is missing"}, 400)

        project = Project.objects.filter(id=project_id).first()
        if project is None:
            return Response({"error": "project=%s not found" % project_id}, 404)

        data = Data.objects.filter(dataset=project.dataset.id).all()
        ret = []

        label = Label.objects.filter(project=project).all()
        data = DataSerializer(data, many=True)
        label = LabelSerializer(label, many=True)
        label = {x['id']:x for x in label.data}

        for d in data.data:
            datum = {}
            datum['data'] = d
            datum['label'] = label.get(d['id'], None)
            ret.append(datum) 

        return Response({"data": ret})

    def post(self, request, format=None):
        project = Project.objects.filter(id=request.data.get('project')).first()
        data_id = request.data.get('dat')
        data = Data.objects.filter(id__in=data_id).all()

        if project is None:
            return Response({"error": "project not found"}, status=404)

        if len(data) != len(data_id):
            return Response({"error": "not all data is found"}, status=404)

        for dat in data:
            print(dat.id)
            label = Label.objects.filter(project=project, dat=dat).first()
            if label is not None:
                label.config = json.dumps(request.data.get('config', '{}'))
                label.save()
            else:
                label = Label(  project=project,
                                dat=dat,
                                config=json.dumps(request.data.get('config', '{}')))
                label.save()

        return Response(status=204)


class DataLabel(APIView):
    def get(self, request, format=None):
        project_id = request.GET.get('project')
        if project_id is None:
            return Response({"error": "project is missing"}, 400)

        project = Project.objects.filter(id=project_id).first()
        if project is None:
            return Response({"error": "project=%s not found" % project_id}, 404)

        search = request.GET.get('search')
        encode = request.GET.get('encode', '0')

        if search:
            if encode == '1':
                search = base64.b64decode(search).decode('utf8')
            print(search)
            search = expression.jsep(search).parsed

        datas = Data.objects.filter(dataset=project.dataset).all()
        labels = Label.objects.filter(project=project).all()

        dataSerializers = DataSerializer(datas, many=True)
        lblSerializers = LabelSerializer(labels, many=True)

        response = []
        for d in dataSerializers.data:
            resp = {}
            resp['data'] = d
            for lbl in labels:
                if lbl.dat.id == d['id']:
                    resp['label'] = LabelSerializer(lbl).data
                    break

            response.append(resp)

        if search:
            response = [r for r in response if expression.applyExpression({"data": r}, search)]

        return Response(response)
