from django.db import models
from datasets.models import Dataset
# Create your models here.
class Data(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    path = models.TextField(blank=False)
    datatype = models.CharField(
        max_length=10,
        choices=(
            ("image", 'Image'),
        ),
        default="image",
    )
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('created',)
