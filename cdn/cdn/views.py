from django.shortcuts import render

def index(request):
    applications = {
        "stat_cdnnow/": "Получение статистики трафика через API",
        "traffic_metric/": "Получение метрик трафика через API",
        "test_images/": "Проверка загрузки изображений через CDN",
        "test_cash/": "Проверка кеширования контента в CDN",
        "log_analize/": "Анализ лог файла CDN" 
    }
    context = {
        "applications": applications
    }
    return render(request, "cdn/index.html", context=context)