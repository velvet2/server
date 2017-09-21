from datasets.models import Dataset
from datasets.serializers import DatasetSerializer
from projects.models import Project
from labels.models import Label
from datas.models import Data
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import status
from datas.models import Data
from datas.serializers import DataSerializer
from django.http import HttpResponse
import io
import zipfile
import json

class DatasetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response({"data": serializer.data})

    def post(self, request, format=None):
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username = 'root', password = 'abc123123')
            serializer.save(owner=user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DatasetDetail(APIView):
    def get_object(self, pk):
        try:
            return Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        search = request.GET.get('search')
        print(search)
        dataset = self.get_object(pk)
        serializer = DatasetSerializer(dataset)
        serializedData = DataSerializer(Data.objects.filter(dataset=dataset), many=True)

        return Response({"data": serializedData.data})

    def put(self, request, pk, format=None):
        dataset = self.get_object(pk)
        serializer = DatasetSerializer(dataset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dataset = self.get_object(pk)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DatasetExport(APIView):
    def get(self, request, pk):
        manifest = {}
        dataset = Dataset.objects.get(pk=pk)
        manifest['name'] = dataset.name
        data = Data.objects.filter(dataset=pk).order_by('id').all()

        data_json = []
        for dat in data:
            path = '/'.join(dat.path.split('/')[2:]) + '/' + dat.name
            data_json.append({
                'id': dat.id,
                'path': path,
                'type': dat.datatype
            })

        byte_stream = io.BytesIO()
        zip_ob = zipfile.ZipFile(byte_stream, 'w')
        zip_ob.writestr('data/data.json', json.dumps(data_json, indent=2))
        manifest['data'] = { 'include' : 'data/data.json'}

        projects = Project.objects.filter(dataset=pk).order_by('id').all()
        manifest['label'] = []
        for project in projects:
            filename = '%s.json' % project.name
            label_json = []
            labels = Label.objects.filter(project=project).order_by('dat__id').all()
            for lbl in labels:
                label_json.append({
                    'id': lbl.dat.id,
                    'config': json.loads(lbl.config)
                })

            manifest['label'].append({
                'name': project.name,
                'include': 'label/%s' % filename
            })

            zip_ob.writestr('label/%s' % filename, json.dumps(label_json, indent=2))

        zip_ob.writestr('manifest.json', json.dumps(manifest, indent=2))
        zip_ob.close()
        byte_stream.seek(0)

        response = HttpResponse(byte_stream)
        response['Content-Disposition'] = 'attachment; filename=data.zip'

        return response
