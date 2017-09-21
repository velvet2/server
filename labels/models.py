from django.db import models
from datas.models import Data
from projects.models import Project

# Create your models here.
class Label(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    config = models.TextField(blank=False)
    project = models.ForeignKey(
        Project,
        related_name='projects',
        on_delete=models.CASCADE,
    )

    dat = models.ForeignKey(
        Data,
        related_name='datas',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('created',)
