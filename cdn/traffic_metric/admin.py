from django.contrib import admin
from .models import Metric_settings, Metrics, Projects, Granularity

admin.site.register(Metric_settings)
admin.site.register(Metrics)
admin.site.register(Projects)
admin.site.register(Granularity)
