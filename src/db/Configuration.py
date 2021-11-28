from pymongo import MongoClient
import ssl 

class Configuration(object):
    def __init__(self, config):
        self.login = config["MONGO_CLUSTER_LOGIN"]
        self.password = config["MONGO_CLUSTER_PASSWORD"]
        self.dbName = config["MONGO_CLUSTER_DB_NAME"]
        self.cluster = config["MONGO_CLUSTER_NAME"]

    def get_collection(self,collectionName):
        str_conn = f'mongodb+srv://{self.login}:{self.password}@{self.cluster}'
        return MongoClient(str_conn, ssl_cert_reqs=ssl.CERT_NONE)[self.dbName][collectionName]
    

    