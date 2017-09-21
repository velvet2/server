from datasets.models import Dataset
from projects.models import Project
from projects.serializers import ProjectSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import status
# from datas.serializers import DataSerializer
from projects.serializers import ProjectSerializer
import json

class ProjectList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        datasets = Project.objects.all()
        serializer = ProjectSerializer(datasets, many=True)
        return Response({"data": serializer.data})

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username = 'root', password = 'abc123123')
            print(user)
            serializer.save(owner=user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        serializedData = ProjectSerializer(project)
        return Response({"data": serializedData.data})

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        print(
            project.name
        )
        project.name = request.data.get('name', project.name)
        config = request.data.get('config')
        if config != None:
            project.config = json.dumps(config)

        project.save()
        return Response(status=202)

    def delete(self, request, pk, format=None):
        dataset = self.get_object(pk)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectExport(APIView):
    def get(self, request, pk):
        return Response({})
