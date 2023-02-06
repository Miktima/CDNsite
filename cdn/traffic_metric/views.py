from django.shortcuts import render
from .models import Projects
from datetime import date
from .Traffic import Trafficsite
import pandas as pd
import json
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from io import BytesIO
import base64

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

def index(request):
    project_list = Projects.objects.all()
    years = [2021, 2022, 2023]
    months = []
    for i in range (1, 13):
        months.append(i)
    days = []
    for i in range (1, 32):
        days.append(i)
    td = date.today()
    current_year = int(td.strftime("%Y"))
    current_month = int(td.strftime("%m"))
    current_day = int(td.strftime("%d"))
    context = {
        'project_list': project_list,
        'years': years,
        'months': months,
        'days': days,
        'current_year': current_year,
        'current_month': current_month,
        'current_day': current_day
    }
    return render(request, "traffic_metric/index.html", context)

def results(request):
    project = request.POST['project']
    try:
        project_obj = Projects.objects.get(name=project)
    except Projects.DoesNotExist:
        # Redisplay the form.
        messages.error(request, 'Необходимо выбрать проект')
        return HttpResponseRedirect(reverse('index'))
    else:
        from_date = date(int(request.POST['from_year']), int(request.POST['from_month']), int(request.POST['from_day']))
        to_date = date(int(request.POST['to_year']), int(request.POST['to_month']), int(request.POST['to_day']))
        if from_date > to_date:
            messages.error(request, 'Дата начала периода должна быть меньше даты окончания')
            return HttpResponseRedirect(reverse('index'))        
        objTraffic = Trafficsite()
        if objTraffic.get_traffic_metric(project, from_date, to_date) != False:
            result = objTraffic.get_traffic_metric(project, from_date, to_date)
        else:
            messages.error(request, objTraffic.error)
            return HttpResponseRedirect(reverse('index'))        
        result_frame = pd.read_json(json.dumps(result), "records")
        locator = mdates.AutoDateLocator(minticks=5, maxticks=9)
        formatter = mdates.ConciseDateFormatter(locator)
        # 1 plot
        fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(result_frame["timestamp"], result_frame["edge_cache_status_hit_ratio"])
        ax.set_title("Edge cache status hit ratio") 
        img1_in_memory = BytesIO()
        plt.savefig(img1_in_memory, format="png")
        edge_cache = base64.b64encode(img1_in_memory.getvalue()).decode()
        plt.clf()
        # 2 plot
        fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(result_frame["timestamp"], result_frame["edge_requests_count"], label="edge requests count")
        ax.plot(result_frame["timestamp"], result_frame["edge_status_4xx"], label="edge status 4xx")
        ax.set_title("Edge requests") 
        ax.legend()
        img2_in_memory = BytesIO()
        plt.savefig(img2_in_memory, format="png")
        edge_requests = base64.b64encode(img2_in_memory.getvalue()).decode()
        plt.clf()
        # 3 plot
        fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(result_frame["timestamp"], result_frame["origin_requests_count"], label="origin requests count")
        ax.plot(result_frame["timestamp"], result_frame["origin_status_4xx"], label="origin status 4xx")
        ax.set_title("Origin requests") 
        ax.legend()
        img3_in_memory = BytesIO()
        plt.savefig(img3_in_memory, format="png")
        origin_requests = base64.b64encode(img3_in_memory.getvalue()).decode()
        plt.clf()
        # 4 plot
        result_frame["ratio_requests_count"] = result_frame["edge_requests_count"] / result_frame["origin_requests_count"]
        result_frame["ratio_status_4xx"] = result_frame["edge_status_4xx"] / result_frame["origin_status_4xx"]
        fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(result_frame["timestamp"], result_frame["ratio_requests_count"], label="ratio requests count")
        ax.plot(result_frame["timestamp"], result_frame["ratio_status_4xx"], label="ratio status 4xx")
        ax.set_title("Ratio of edge requests count to origin ones")
        ax.legend() 
        img4_in_memory = BytesIO()
        plt.savefig(img4_in_memory, format="png")
        ratio_requests = base64.b64encode(img4_in_memory.getvalue()).decode()
        plt.clf()
        context = {
            "plot_edge_cash": edge_cache,
            "plot_edge_requests": edge_requests,
            "plot_origin_requests": origin_requests,
            "plot_ratio_requests": ratio_requests,
            "origin": project_obj.origin,
            "from_date": from_date.strftime("%d/%m/%Y"),
            "to_date": to_date.strftime("%d/%m/%Y")
        }
        return render(request, 'traffic_metric/results.html', context)
