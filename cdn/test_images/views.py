from django.shortcuts import render
from .forms import CdnForm
from django.http import HttpResponseRedirect
from django.contrib import messages
import requests
import re
import time

def index(request):
    form = CdnForm()
    return render(request, "test_images/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = CdnForm(request.POST)
        if form.is_valid():
            page_url = request.POST['page_url']
            old_cdn = request.POST['old_cdn']
            if request.POST['new_cdn'] != "":
                new_cdn = request.POST['new_cdn']
            else:
                new_cdn = old_cdn
            response = requests.get(page_url)
            if response.status_code != 200:
                messages.error(request, 'The page cannot be loaded!')
                form = CdnForm()
                return render(request, "test_images/index.html", {'form': form})
            source = response.text
            # Domain of the page
            # domain = (re.search("^https://([A-Za-z_0-9.-]+).*", page_url)).group(1)
            # The regular expression for select CDN part
            # regexp_cdn_domain = "cdnn\d.img." + domain + "/?([^<?\'\\\" >]+)"
            regexp_cdn_domain = old_cdn + "/?([^<?\'\\\" >]+)"
            links_list = []
            links_list = re.findall(regexp_cdn_domain, source)
            newcdn_links_list = []
            for l in links_list:
                if re.search("[a-z]$", l) != None:
                    newcdn_links_list.append("https://" + new_cdn + "/" + l)
            n_all = 0
            n_err = 0
            bad_list = []
            for l in newcdn_links_list:
                response_image = requests.get(l)
                status = response_image.status_code
                n_all += 1
                time.sleep(0.3)
                if status != 200:
                    bad_list.append([l, status])
                    n_err += 1
            conclusion = "Errors {0:d} from {1:d} urls ({2:.1f}%)".format(n_err, n_all, (n_err/n_all)*100)
            context = {
                "new_cdn": new_cdn,
                "old_cdn": old_cdn,
                "conclusion": conclusion,
                "bad_list": bad_list
            }
            return render(request, 'test_images/results.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CdnForm()
        return render(request, "test_images/index.html", {'form': form})

