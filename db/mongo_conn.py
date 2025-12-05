from pymongo import MongoClient

MONGO_URI = "mongodb+srv://admin:rI6RCQ1eq5ca91WD@cluster0.vvaxbv1.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

def get_db():
    return client["ProyectoBonos"]
