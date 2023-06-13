import requests
import re
from test_cash.models import Cash_settings
from stat_cdnnow.models import Portals_stat

class ClearCache:
    def __init__(self, portal):
    # Определяем параметры запросов
        settings = Cash_settings.objects.first()
        self.login = settings.login
        self.password = settings.password
        self.cdnnow_urlauth = settings.url_auth
        self.cdnnow_url_request = re.sub("validity", "cache-clear", settings.url_request)
        self.cdnnow_url_request = re.sub("/v4/cache", "/v1/projects", self.cdnnow_url_request)
        self.error = ""
        # получаем идентификатор для домена - домен должен быть в базе данных
        try:
            portal_obj = Portals_stat.objects.get(portal=portal)
        except Portals_stat.DoesNotExist:
            self.error = 'Идентификатор для домена ' + portal + ' не найден'
        else:
            self.id_portal = portal_obj.id_portal

    def get_token(self):
        # Получаем токен для последующих запросов
        login_data = {
            'username': self.login,
            'password': self.password
        }
        response = requests.post(self.cdnnow_urlauth, data = login_data)
        if (response.json())["status"] != "ok":
            self.error = "ERROR: response status:", response.json()
            return False
        else:
            data = (response.json())["data"]
            return data["token"]
    
    def clear_cache(self, token, masks:list):
        # запрос на очистку кеша
        url = (self.cdnnow_url_request).replace("##portal##", self.id_portal)
        print ("url: ", url)
        print ("token: ", token)
        print ("masks:")
        if len(masks) == 0:
            print("       no elements")
        else:
            for m in masks:
                print("         ",m)
        if len(masks) == 0:
            response = requests.post(url, headers = {'token': token})
        else:
            # response = requests.post(url, headers = {'token': token}, data={'masks': masks})
            response = requests.post(url, headers = {'token': token}, data={'masks': '/css/*'})
            # response = requests.post(url, data={'masks': masks, 'token': token})
        print ("response: ", response.text)
        if (response.json())["status"] == "ok":
            return True
        else:
            self.error = "ERROR: response: " + str(response)
            return False
    
