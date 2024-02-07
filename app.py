from pymongo import MongoClient
import json
from bson import ObjectId
import bson.errors
import time 


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


# Buscar CV por ID
def buscar_cv_por_id(collection):
    cv_id = input("Ingrese el ID del currículum a buscar: ").strip()

    try:
        cv_object_id = ObjectId(cv_id)
        result = collection.find_one({"_id": cv_object_id})

        if result:
            print("\nCurrículum encontrado:")
            print(f"ID: {result['_id']}")
            print(f"Nombre: {result['datos_personales']['nombre']} {result['datos_personales']['apellido']}")
            
            # Utilizar get para manejar la posible falta de la clave 'direccion'
            direccion = result['datos_personales'].get('direccion', {})
            pais = direccion.get('pais', 'No disponible')
            estado = direccion.get('estado', 'No disponible')
            ciudad = direccion.get('ciudad', 'No disponible')
            
            print(f"Dirección: {pais}, {estado}, {ciudad}")
            
            # Utilizar get para manejar la posible falta de la clave 'telefono'
            telefonos = result['datos_personales'].get('telefono', [])
            print(f"Teléfono: {', '.join(telefonos) if telefonos else 'No disponible'}")
            
            # Utilizar get para manejar la posible falta de la clave 'email'
            email = result['datos_personales'].get('email', 'No disponible')
            print(f"Email: {email}")
            
            # Manejar la posible falta de la clave 'redes' en 'datos_personales'
            redes_sociales = result['datos_personales'].get('redes', {})
            
            print(f"Redes Sociales: Facebook - {redes_sociales.get('facebook', 'No disponible')}, "
                  f"Instagram - {redes_sociales.get('instagram', 'No disponible')}, "
                  f"GitHub - {redes_sociales.get('github', 'No disponible')}")
            
            print("\nEducación:")
            print(f"Nivel: {result['educacion']['nivel']}")
            print(f"Título: {', '.join(result['educacion']['titulo'])}")
            print(f"Institución: {', '.join(result['educacion']['institucion'])}")
            print("\nHabilidades:")
            
            # Utilizar get para manejar la posible falta de la clave 'habilidades'
            habilidades = result.get('habilidades', [])
            print(', '.join(habilidades))
            
            print("\nIntereses:")
            
            # Utilizar get para manejar la posible falta de la clave 'intereses'
            intereses = result.get('intereses', [])
            print(', '.join(intereses))
        else:
            print(f"No se encontró ningún currículum con el ID: {cv_id}")
    except (ValueError, bson.errors.InvalidId):
        print("ID no válido. Por favor, ingrese un ID de currículum válido.")



#Eliminar CV por ID 
def eliminar_cv_por_id(collection):
    cv_id = input("\nIngrese el ID del currículum a eliminar: ")

    try:
        cv_object_id = ObjectId(cv_id)
        result = collection.delete_one({"_id": cv_object_id})

        if result.deleted_count > 0:
            print(f"Se eliminó correctamente el currículum con ID: {cv_id}")
        else:
            print(f"No se encontró ningún currículum con el ID: {cv_id}")
    except (ValueError, bson.errors.InvalidId):
        print("ID no válido. Por favor, ingrese un ID de currículum válido.")


#Imprimir todos los CVs
def mostrar_todos_cv(collection):
    print("\n== Todos los Currículums ==")
    
    cursor = collection.find()

    for curr in cursor:
        print("\nCurrículum:")
        print(f"ID: {curr['_id']}")
        print(f"Nombre: {curr['datos_personales']['nombre']} {curr['datos_personales']['apellido']}")
        
        # Utilizar get para manejar la posible falta de la clave 'telefono'
        telefonos = curr['datos_personales'].get('telefono', [])
        print(f"Teléfono: {', '.join(telefonos) if telefonos else 'No disponible'}")
        
        # Utilizar get para manejar la posible falta de la clave 'email'
        email = curr['datos_personales'].get('email', 'No disponible')
        print(f"Email: {email}")
        
        # Manejar el caso en que no exista la clave 'redes' en el documento
        redes_sociales = curr['datos_personales'].get('redes', {})
        
        print(f"Redes Sociales: Facebook - {redes_sociales.get('facebook', 'No disponible')}, "
              f"Instagram - {redes_sociales.get('instagram', 'No disponible')}, "
              f"GitHub - {redes_sociales.get('github', 'No disponible')}")
        
        print("\nEducación:")
        print(f"Nivel: {curr['educacion']['nivel']}")
        print(f"Título: {', '.join(curr['educacion']['titulo'])}")
        print(f"Institución: {', '.join(curr['educacion']['institucion'])}")
        print("\nHabilidades:")
        
        # Utilizar get para manejar la posible falta de la clave 'habilidades'
        habilidades = curr.get('habilidades', [])
        print(', '.join(habilidades))
        
        print("\nIntereses:")
        
        # Utilizar get para manejar la posible falta de la clave 'intereses'
        intereses = curr.get('intereses', [])
        print(', '.join(intereses))
        print("\n-----------------------------")

    print("Fin de la lista de currículums.\n")


#PONER AQUÍ LAS FUNCIONES DE AGREGAR CV


#Opciones del menú
def show_menu():
    print("\n== Menú de Operaciones ==")
    print("Seleccione una opción:")
    print("1. Creación de CV")
    print("2. Actualización de CV")
    print("3. Eliminación de CV")
    print("4. Buscar CV")
    print("5. Mostrar todos los CVs")
    print("6. Intereses más comunes")
    print("7. Herramientas manejadas por cada individuo")
    print("8. Trabajos realizados")
    print("9. Salir")
    print("=========================")


#Conexion con la BD
collection = connect_to_mongodb()

#Programa principal
def main():

    # Insertar datos al inicio del programa (solo si no se han insertado antes)
    insert_data(collection)

    while True:
        show_menu()

        try:
            opcion = int(input("Ingrese opción => "))
            if opcion == 1:
                print("opcion 1")
            elif opcion == 2:
                print("opcion 1")
            elif opcion == 3:
                eliminar_cv_por_id(collection)
            elif opcion == 4:
                buscar_cv_por_id(collection)
            elif opcion == 5:
                mostrar_todos_cv(collection)
            elif opcion == 6:
                print("opcion 1")
            elif opcion == 7:
                print("opcion 1")
            elif opcion == 8:
                print("opcion 1")
            elif opcion == 9:
                print("Saliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, elija una opción válida.")
        except ValueError:
            print("Por favor, ingrese un número válido.")


#Main
if __name__ == "__main__":
    main()
