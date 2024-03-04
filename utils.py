import pymssql as msql
from pymongo.mongo_client import MongoClient


def get_connection():
    
    #Create connection to the database
    connection = msql.connect(
            server="animals014.database.windows.net",
            user="ricardo_gonzalez",
            password="Peluche343@",
            database="AnimalsDBL",
    )

    cur = connection.cursor()
    
    return cur

def get_mongo_connection():
        uri = "mongodb+srv://a01770368:Fam32352@cluster0.wc1zlcr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        client = MongoClient(uri)
        db = client['dbCai']
        collection = db['collectionCai']
        
        return collection
