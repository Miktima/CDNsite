from django.contrib import admin
from .models import Metric_settings, Metrics, Projects, Granularity

class Metric_settingsAdmin(admin.ModelAdmin):
     fields = ['token', 'url_metric']

admin.site.register(Metric_settings, Metric_settingsAdmin)
admin.site.register(Metrics)
admin.site.register(Projects)
admin.site.register(Granularity)
