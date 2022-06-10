import logging
import sys
import re 

import sys
import requests
import json
import re
import cgi
from http.server import HTTPServer, SimpleHTTPRequestHandler

from . import tca_db
from . import tca_att

class PythonServer(SimpleHTTPRequestHandler):
    """Python HTTP Server that handles GET and POST requests"""
    def do_POST(self) -> None:
        html = "{'message':'Not support'}"
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(html, "utf-8"))

    def do_GET(self):
        result = re.search("/api/devices/(\d+)", self.path)
        if result is None:
            self.send_response(404)
            self.end_headers()
            return
        
        imei = result.group(1)
        info = get_device_info(imei)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(str(info), "utf-8"))

def get_device_info(imei):
    r""" Gets device info
    
    First of all looks in db for device info, then check atta
    backend.
    """
    if tca_db.has_device_info(imei):
        return tca_db.get_device_info(imei)
    device_info = tca_att.get_device_info(imei)
    if device_info is not None:
        tca_db.save_device_info(imei, device_info)
    return device_info

