from django.shortcuts import render
from .forms import DnsForm
import socket

def index(request):
    form = DnsForm()
    return render(request, "dnsheader/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = DnsForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data["domain"]
            cdn = form.cleaned_data["cdn"]
            d_domain = socket.getfqdn(domain)
            d_cdn = socket.getfqdn(cdn)
            context = {
                "domain": domain,
                "data_domain": d_domain,
                "data_cdn": d_cdn
            }
            return render(request, 'dnsheader/results.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = DnsForm()
        return render(request, "dnsheader/index.html", {'form': form})
