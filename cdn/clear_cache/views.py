from django.shortcuts import render
from .forms import ClearCacheForm
from .ClearCache import ClearCache
from django.contrib import messages
from stat_cdnnow.models import Portals_stat


def index(request):
    form = ClearCacheForm()
    return render(request, "clear_cache/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = ClearCacheForm(request.POST)
        if form.is_valid():
            project = request.POST['project']
            portal_ins = Portals_stat.objects.get(pk=project)
            portal = portal_ins.portal
            masks_field = request.POST['masks']
            # формируем лист масок
            masks = []
            if len(masks_field) > 0:
                masks = masks_field.split(",")
            # При инициализации класса создаются переменные для запроса, включая идентификатор домена в CDN
            # Если идентификатор не найден, возвращаемся на страницу запроса
            if ClearCache(portal) != False:
                objClearCache = ClearCache(portal)
            else:
                messages.error(request, ClearCache(portal).error)
                form = ClearCacheForm()
                return render(request, "clear_cache/index.html", {'form': form})
            if objClearCache.get_token() != False:
                token = objClearCache.get_token()
                # Очищаем кеш по маске
                response = objClearCache.clear_cache(token, masks)
            else:
                messages.error(request, "Невозможно получить токен")
                form = ClearCacheForm()
                return render(request, "clear_cache/index.html", {'form': form})
        context = {
            "portal": portal,
            "response": response
        }
        return render(request, "clear_cache/results.html", context)
    else:
        form = ClearCacheForm()
        return render(request, "clear_cache/index.html", {'form': form})
