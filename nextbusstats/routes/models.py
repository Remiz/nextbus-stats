from __future__ import unicode_literals
from django_pandas.managers import DataFrameManager
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


class Direction(models.Model):
    tag = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    stops = models.ManyToManyField('Stop', through='DirectionStop')
    route = models.ForeignKey('Route', on_delete=models.CASCADE, related_name='directions')

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


class DirectionStop(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    position = models.IntegerField()


class Prediction(models.Model):
    posted_at = models.DateTimeField(auto_now_add=True)
    seconds = models.IntegerField()
    stop = models.ForeignKey('Stop', on_delete=models.CASCADE, related_name='predictions')

    objects = DataFrameManager()

    def __str__(self):
        return "%s - %s s - %s" % (self.stop, self.seconds, self.posted_at)
