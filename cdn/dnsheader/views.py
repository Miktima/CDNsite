import dns.resolver
import re
import requests
from django.shortcuts import render
from .forms import DnsForm



def index(request):
    form = DnsForm()
    return render(request, "dnsheader/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = DnsForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data["domain"]
            cdn = form.cleaned_data["cdn"]
            # Результаты сохраняем в лист
            result_domain = []
            result_http = []
            # Получаем результаты для домена с img. и без .img
            response = requests.get("https://" + domain, verify=False)
            result_http.append({
                "url": "https://" + domain,
                "status_code": response.status_code,
                "history": response.history,
                "headers": response.headers
            })
            try:
                result_domain.append({
                    "query": True,
                    "result": dns.resolver.resolve(domain, 'A')
                })
            except  dns.resolver.NXDOMAIN:
                result_domain.append({
                    "query": False,
                    "qname": domain,
                    "error": "NXDOMAIN: The DNS query name does not exist"
                })
            if re.search("^img.*", domain):
                domain = domain.replace("img.", "")
            else:
                domain = "img." + domain
            result_http.append({
                "url": "https://" + domain,
                "status_code": response.status_code,
                "history": response.history,
                "headers": response.headers
            })
            try:
                result_domain.append({
                    "query": True,
                    "result": dns.resolver.resolve(domain, 'A')
                })
            except  dns.resolver.NXDOMAIN:
                result_domain.append({
                    "query": False,
                    "qname": domain,
                    "error": "NXDOMAIN: The DNS query name does not exist"
                })                
            # Если в списке cdn нет запятой, то указан один адрес. Если есть, то несколько
            result_cdn = []
            if cdn.find(",") >0:
                cdn_list = cdn.split(",")
                for c in cdn_list:
                    try:
                        result_cdn.append({
                            "query": True,
                            "result": dns.resolver.resolve(c.strip(), 'A')
                        })
                    except  dns.resolver.NXDOMAIN:
                        result_cdn.append({
                            "query": False,
                            "qname": c.strip(),
                            "error": "NXDOMAIN: The DNS query name does not exist"
                        })                
            else:
                try:
                    result_cdn.append({
                        "query": True,
                        "result": dns.resolver.resolve(cdn, 'A')
                        })
                except  dns.resolver.NXDOMAIN:
                    result_cdn.append({
                        "query": False,
                        "qname": cdn,
                        "error": "NXDOMAIN: The DNS query name does not exist"
                    })
                     
            context = {
                "domain": domain,
                "result_domain": result_domain,
                "result_cdn": result_cdn,
                "result_http": result_http,
            }
            return render(request, 'dnsheader/results.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = DnsForm()
        return render(request, "dnsheader/index.html", {'form': form})
