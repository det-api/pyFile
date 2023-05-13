from db_config.connection import DB_CONNECT

class Query :

    def addOne (dictData) :
        if type(dictData) is dict :
            DB_CONNECT.connect()
            if DB_CONNECT.get_connection() :
                collection = DB_CONNECT.get_collection()
                result = collection.insert_one(dictData)
                DB_CONNECT.disconnect()
                return {"message":"Success Add One!", "data":result}

    def getOne (filterData) :
        if type(filterData) is dict :
            DB_CONNECT.connect()
            if DB_CONNECT.get_connection() :
                collection = DB_CONNECT.get_collection()
                result = collection.find_one(filterData)
                DB_CONNECT.disconnect()
                return {"message":"Success Get One!", "data":result}
            
    def updateOne (filterData) :
        if type(filterData) is dict :
            DB_CONNECT.connect()
            if DB_CONNECT.get_connection() :
                collection = DB_CONNECT.get_collection()
                result = collection.update_one(filterData, {"$set":{"sync_already":1}})
                DB_CONNECT.disconnect()
                return {"message":"Success Update One!", "data":result}

    



