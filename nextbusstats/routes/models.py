from __future__ import unicode_literals

from django.db import models


class Route(models.Model):
    tag = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=6)
    opposite_color = models.CharField(max_length=6)
    lat_min = models.FloatField()
    lat_max = models.FloatField()
    lon_min = models.FloatField()
    lon_max = models.FloatField()
    monitored = models.BooleanField(default=False)

    class Meta:
        ordering = ['tag']

    def __str__(self):
        return self.title


class Stop(models.Model):
    tag = models.CharField(max_length=10)
    stop_id = models.CharField(max_length=10, null=True)
    title = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    route = models.ForeignKey('Route', on_delete=models.CASCADE, related_name='stops')

    class Meta:
        ordering = ['tag']

    def __str__(self):
        return self.title
