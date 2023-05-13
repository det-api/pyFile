import pymongo
from constants import Constants

class DB_CONNECT :
    
    def connect () :
        global connection 
        global collection
        
        connection = pymongo.MongoClient(Constants.DB_HOST, Constants.DB_PORT)
        database = connection[Constants.DB_NAME]
        collection = database[Constants.DB_TABLE_NAME]
    
    def disconnect () :
        global connection
        if connection :
            connection.close()

    def get_connection () :
        global connection 
        return connection

    def get_collection () :
        global collection 
        return collection