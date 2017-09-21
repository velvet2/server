import os
from datasets.models import Dataset
from datas.models import Data
from datas.serializers import DataSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import status
from server import settings

class DataList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, dataset_id=None, format=None):
        filt = request.GET.get('search')
        datasets = Data.objects.all()
        serializer = DataSerializer(datasets, many=True)

        return Response({"data": serializer.data})

    def post(self, request, dataset_id=None, format=None):
        path = request.POST.get('path', None)
        data = request.FILES.get('file', None)

        if path is None or data is None:
            return Response({"error": "path are not defined" },
                            status=status.HTTP_400_BAD_REQUEST)

        dataset = Dataset.objects.filter(id = dataset_id).first()
        if dataset == None:
            return Response({"error": "id %s does not exists" % dataset_id},
                            status=status.HTTP_404_NOT_FOUND)

        upload_path = '%s/%s/%s' % ( settings.UPLOAD_URL, dataset_id, os.path.normpath(path))
        upload_path = os.path.normpath(upload_path)
        if os.path.isdir(upload_path) != True:
            os.makedirs(upload_path)

        with open('%s/%s' % ( upload_path, data.name ), 'wb+') as destination:
            for chunk in data.chunks():
                destination.write(chunk)

        data = Data(name=data.name, dataset=dataset, path=upload_path)
        data.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
