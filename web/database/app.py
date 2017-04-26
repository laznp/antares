import random, string
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo = MongoClient()
dbMongo = mongo['antares']

class app(object):
    ID = '_id'
    APP_DIR = 'app_dir'
    APP_DOMAIN ='app_domain'
    APP_HOST = 'app_host'
    APP_NAME = 'app_name'
    APP_REPO = 'app_repo'
    APP_ENV = 'app_env'

    def find_one(self,*dict):
        return dbMongo.antares_app.find_one(*dict)

    def find(self, *dict):
        return dbMongo.antares_app.find(*dict)

    def insert_one(self, *dict):
        return dbMongo.antares_app.insert_one(*dict).inserted_id

    def delete_one(self, *dict):
        return dbMongo.antares_app.delete_one(*dict)

    def update(self,*dict):
        return dbMongo.antares_app.update(*dict)


# App = app()
# inserted_id = App.delete_one({"ssss":"aaa"})
# print str(inserted_id.raw_result)
