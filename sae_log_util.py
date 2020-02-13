#-*-coding: utf8 -*-

#sae_log_util.py
#sae log utility based on sae apibus_handler
#author blog: http://bookshadow.com
#src date: 2015-09-17

status_code_dict = {200 : 'OK', 206 : 'Partial Content', 400 : 'Bad Request', \
                              500 : 'Internal Server Error' , 404 : 'Not Found'}

service_ident_dict = {'http': ['access', 'error', 'alert', 'debug', 'warning', 'notice'], \
    'taskqueue' : ['error'], \
    'cron' : ['error'], \
    'mail': ['access', 'error'], \
    'rdc' : ['error', 'warning'], \
    'storage' : ['access'], \
    'push' : ['access'], \
    'fetchurl' : ['access']
}

_URL_PREFIX = 'http://g.sae.sina.com.cn/log/'

class SaeLogFetcher(object):

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
    
    def fetch_log(self, service, date, ident, fop = '', version = 1):
        assert self.access_key, 'access_key should not be empty'
        assert self.secret_key, 'secret_key should not be empty'
        assert service in service_ident_dict, 'invalid service parameter'
        assert ident in service_ident_dict[service], 'invalid ident parameter'

        url = _URL_PREFIX + service + '/' + date + '/' + str(version) + '-' + ident + '.log'
        content = None

        try:
            import requests
            from apibus_handler import SaeApibusAuth
            r = requests.get(url + ('?' + fop if fop else ''), \
                     auth=SaeApibusAuth(self.access_key, self.secret_key))
            status_code, status = r.status_code, status_code_dict.get(r.status_code, 'Unknown')
            if status_code == 200:
                content = r.content
        except ImportError:
            # requests was not present!
            from apibus_handler import SaeApibusAuthHandler
            import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
            apibus_handler = SaeApibusAuthHandler(self.access_key, self.secret_key)
            opener = urllib.request.build_opener(apibus_handler)
            if fop:
                url += '?' + urllib.parse.quote(fop, safe='')
            content = opener.open(url).read()
        return content