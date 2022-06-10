import pymongo
from pip._vendor.pyparsing.core import dbl_quoted_string
import imeiminer.imei
import logging
import os

logger = logging.getLogger(__name__)

db = None
client = None
mongo_uri = os.getenv("DB_URL", "mongodb://root:root@localhost:27017")
mongo_db = os.getenv("DB_NAME", "moee")

    
def get_db():
    global db
    global mongo_uri
    global clint
    
    if db is not None:
        return db
    # DB connection
    client = pymongo.MongoClient(mongo_uri)
    db = client[mongo_db]
    return db


def has_device_info(imei):
    device_info = get_device_info(imei)
    if device_info is None:
        return False
    return True


def get_device_info(imei):
    db = get_db()
    collection = db['tcas']
    tca = imeiminer.imei.get_tca(imei)
    device_info = collection.find_one({'tca': tca})
    if device_info is None:
        return None
    return device_info


def save_device_info(imei, device_info):
    db = get_db()
    collection = db['tcas']
    tca = imeiminer.imei.get_tca(imei)
    device_info['tca'] = tca
    collection.update_one(
        filter={
        'tca': tca
        },
        update={
            '$set':device_info
        },
        upsert=True,
        bypass_document_validation=True)
    
