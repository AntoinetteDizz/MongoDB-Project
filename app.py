from pymongo import MongoClient
import json
from bson import ObjectId
import bson.errors


# Datos de conexión a MongoDB
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'cv'
COLLECTION_NAME = 'curriculums'


#Conexión de BD
def connect_to_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection


#Insertar curriculums a la BD
def insert_data(collection):
    # Verificar si ya se han insertado datos
    if collection.count_documents({}) == 0:
        with open('cv.json', 'r') as file:
            curriculums_data = json.load(file)
        result = collection.insert_many(curriculums_data)
        print(f"Se insertaron {len(result.inserted_ids)} documentos en la base de datos.")
    else:
        print("Los datos ya han sido insertados anteriormente.")


#Buscar CV por código
def buscar_cv_por_id(collection):
    cv_id = input("Ingrese el ID del currículum a buscar: ")

    try:
        cv_object_id = ObjectId(cv_id)
        result = collection.find_one({"_id": cv_object_id})

        if result:
            print("Currículum encontrado:")
            print(result)
        else:
            print(f"No se encontró ningún currículum con el ID: {cv_id}")
    except (ValueError, bson.errors.InvalidId):
        print("ID no válido. Por favor, ingrese un ID de currículum válido.")


#Opciones del menú
def show_menu():
    print("Selecciona una opción:")
    print("1. Creacion de CV")
    print("2. Actualizacion de CV")
    print("3. Eliminacion de CV")
    print("4. Buscar CV")
    print("5. Intereses mas comunes")
    print("6. Herramientas manejadas por cada individuo")
    print("7. Trabajos realizados")
    print("8. Salir")


#Programa
def main():
    collection = connect_to_mongodb()

    # Insertar datos al inicio del programa (solo si no se han insertado antes)
    insert_data(collection)

    while True:
        show_menu()

        try:
            opcion = int(input("Ingrese el número de la opción: "))
            if opcion == 1:
                print("opcion 1")
            elif opcion == 2:
                print("opcion 1")
            elif opcion == 3:
                print("opcion 1")
            elif opcion == 4:
                buscar_cv_por_id(collection)
            elif opcion == 5:
                print("opcion 1")
            elif opcion == 6:
                print("opcion 1")
            elif opcion == 7:
                print("opcion 1")
            elif opcion == 8:
                print("Saliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, elija una opción válida.")
        except ValueError:
            print("Por favor, ingrese un número válido.")


#Main
if __name__ == "__main__":
    main()
