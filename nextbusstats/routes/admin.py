from django.contrib import admin
from .models import Route, Stop, Prediction


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('tag', 'title')
    search_fields = ['title']


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ('title', 'route')
    list_filter = ('route',)
    search_fields = ['title']


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    pass
