from django.db import models

# Create your models here.
class Dataset(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='datasets', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)
