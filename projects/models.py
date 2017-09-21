from django.db import models
from datasets.models import Dataset

# Create your models here.
class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='projects', on_delete=models.CASCADE)
    label = models.CharField(
        max_length=10,
        choices=(
            ("class", 'Classification'),
            ("bbox", 'Bounding Box'),
            ("locate", 'Locating')
        ),
        default="class",
    );
    config = models.TextField(blank=False, default='{}')

    class Meta:
        ordering = ('created',)
