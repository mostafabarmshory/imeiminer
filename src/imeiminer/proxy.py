import urllib.request
import certifi
import ssl
import json
import time
import logging
from abc import ABC, abstractmethod

import requests
from pip._vendor.requests.api import request


class Proxy(ABC):
    
    @abstractmethod
    def urlopen(self, url):
        """ Open url and return its content
        
        Open url and read all content as UTF8 text.
        """
        pass
    
    def get_ip(self):
        """ Gets current IP 
        """
        return self.urlopen('https://api.ipify.org?format=json')


class UptimerBotProxy(Proxy):
    """ A proxy to manage remote list of proxy form UptimerBot
    
    UptimerBot is an engine to find free proxy over the net. This class use
    default list of proxy form this bot.
    """
    PROXY_PATH_LIST_URL = 'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt'
    PROXY_UPDATE_INTERVAL = 30 * 60 * 1000
    
    def __init__(self):
        """ Creates new instace of proxy
        """
        logging.info("New instance of proxy is created")
        self.last_update_time = 0
        self.proxy_list = []
        self.counter = 0
    
    def update_proxy_list(self):
        """ Update lisf of proxy
        
        The update function check the last update time. If there is a long time ago
        then the list will update with new one.
        """
        current_time = int(time.time())
        if current_time > self.last_update_time + self.PROXY_UPDATE_INTERVAL:
            logging.info("Download new list of proxy")
            response = requests.get(self.PROXY_PATH_LIST_URL)
            content = response.text
            self.proxy_list = content.split("\n")
            logging.info("Proxy list is updated with new version")
            self.last_update_time = current_time
            self.counter = 0
            
    def get_proxy(self):
        """ Gets next proxy from the list
        It uses a counter and return proxy based on its value.
        """
        self.update_proxy_list()
        proxy = self.proxy_list[self.counter]
        self.counter = (self.counter + 1) % len(self.proxy_list)
        return proxy
    
    def urlopen(self, url):
        response = self.get(url)
        content = response.text
        return content
    
    def get(self, url, params=None, **kwargs):
        r"""Sends a GET request.
    
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        proxy_host = self.get_proxy()
        kwargs.setdefault('proxies', {
            'http': proxy_host,
            'https': proxy_host
        })
        return request('get', url, params=params, **kwargs)
