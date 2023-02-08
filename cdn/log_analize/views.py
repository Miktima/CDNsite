from django.shortcuts import render
from .forms import LogForm
import pandas as pd
from io import BytesIO
import base64
from django.contrib import messages

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def index(request):
    form = LogForm()
    return render(request, "log_analize/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = LogForm(request.POST, request.FILES)
        if form.is_valid():
            log_table = pd.read_csv(request.FILES['file'], ";")
            # request_uri chart
            request_uri_ser = (log_table["request_uri"].value_counts()).head(20)
            request_uri_links = request_uri_ser.to_dict()
            request_uri_values = request_uri_ser.tolist()
            fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
            ax.plot(request_uri_values)
            ax.set_xlabel('Номер позиции')
            ax.set_title("request_uri") 
            request_uri_img = BytesIO()
            plt.savefig(request_uri_img, format="png")
            request_uri_pic = base64.b64encode(request_uri_img.getvalue()).decode()
            plt.clf()
            # http_user_agent chart
            http_user_agent_ser = (log_table["http_user_agent"].value_counts()).head(20)
            http_user_agent_links = http_user_agent_ser.to_dict()
            http_user_agent_values = http_user_agent_ser.tolist()
            fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
            ax.plot(http_user_agent_values)
            ax.set_xlabel('Номер позиции')
            ax.set_title("http_user_agent") 
            http_user_agent_img = BytesIO()
            plt.savefig(http_user_agent_img, format="png")
            http_user_agent_pic = base64.b64encode(http_user_agent_img.getvalue()).decode()
            plt.clf()
            context = {
                "request_uri_plot": request_uri_pic,
                "request_uri_links": request_uri_links,
                "request_uri_values": request_uri_values,
                "http_user_agent_plot": http_user_agent_pic,
                "http_user_agent_links": http_user_agent_links,
                "http_user_agent_values": http_user_agent_values,
            }
            return render(request, "log_analize/results.html", context)
        else:
            form = LogForm()
            messages.error(request, form.errors)
            return render(request, "log_analize/index.html", {'form': form})            
    else:
        form = LogForm()
        return render(request, "log_analize/index.html", {'form': form})

