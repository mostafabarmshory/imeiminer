from imeiminer.proxy import UptimerBotProxy
import logging
import requests.exceptions
import json.decoder
import http.client
import urllib3.exceptions

main_proxy = UptimerBotProxy()


def get_device_info(imei):
    global main_proxy
    url = "https://m.att.com/services/shopwireless/model/att/ecom/api/DeviceInfoActor/setDeviceInfo/?imei=" + imei + "&sim=8930090902203696305"
    retry_counter = 0
    while retry_counter < 3:
        retry_counter += 1
        try:
            response = main_proxy.get(url, headers={
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Sec-GPC": "1",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Hot": "m.att.com",
                "Accept-Language": "en-US,en;q=0.7,fa-IR;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "Upgrade-Insecure-Requests": "1",
                "Accept": "text/html, */*; q=0.01",
                "Content_Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User_Agent":
                        "Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0"
            })
        except:
            logging.warn("Fail to connect to the server. Try with new proxy")
            continue
            
            
            
        if response.status_code != 200:
            logging.info("ATT response is not 200. Try with another proxy")
        
        try: 
            data = response.json()
        except:
            logging.warn("Fail to decode JSON response from ATT. try with another proxy")
            continue
        
        if data['result']['statusName'] != 'Success':
            logging.warn("ATT response is not success. Try with another proxy")
        return data['deviceInfo']
    logging.warn("Fail to get device info from ATT")
    return None
    

if __name__ == '__main__':
    get_device_info("352622996808940")
