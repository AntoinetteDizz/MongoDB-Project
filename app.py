from pymongo import MongoClient
import json

# Datos de conexión a MongoDB
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'cv'
COLLECTION_NAME = 'curriculums'

# Cargar datos desde el archivo JSON
with open('cv.json', 'r') as file:
    curriculums_data = json.load(file)

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Insertar los currículums en la colección
result = collection.insert_many(curriculums_data)

# Imprimir los ID de los documentos insertados
print("IDs de documentos insertados:", result.inserted_ids)

# Cerrar la conexión a MongoDB
client.close()