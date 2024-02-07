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
    
# FUNCION QUE SE ENCARGA DE VERIFICAR SI LA INSERCION FUE EXITOSA 
def verificarInsercion(resultado):
    if resultado.acknowledged:
        print("INSERCION EXITOSA, BAJO EL ID : ",resultado.inserted_id,"\n")
        time.sleep(5)
        return True
    else:
        print("LA INSERCION NO FUE EXITOSA \n")
        time.sleep(3)
        return False

# INGRESA UN DOCUMENTO A LA BASE DE DATOS
    
#FUNCION QUE SE ENCARGA DE RECIBIR UN DOCUMENTO POR PARAMETRO E INGRESARLO A LA BD
def ingresarCV(documento):
    # INSERTA EN LA BD LOS DATOS PREPARADOS CON LA INFORMACION REGISTRADA POR EL USUARIO
    resultado = collection.insert_one(documento)
    verificarInsercion(resultado)

#FUNCION QUE SOLICITA AL USUARIO QUE INGRESE LOS DATOS DEL CV A INGRESAR

def solicitarDatosCV():

    resumen = input("RESUMEN CURRICULAR\n")
    nombre = input("NOMBRE\n")
    apellido = input("APELLIDO\n")

    print("\t\tDATOS DE DIRECCION")

    pais = input("PAIS\n")
    estado = input("ESTADO\n")
    ciudad = input("CIUDAD\n")
    residencia = input("RESIDENCIA\n")

    telefonos = input("TELEFONO, SI TIENE VARIOS SEPARAR CON COMA\n").split(",")
    email = input("EMAIL\n")
    facebook = input("FACEBOOK\n")
    instagram = input("INSTAGRAM\n")
    github = input("GITHUB\n")

    print("\t\tDATOS DE EDUCACION")
    nivel = input("NIVEL DE EDUCACION\n")
    titulos = input("TITULOS QUE POSEE, SEPARADOS POR UNA COMA\n").split(",")
    instituciones = input("INSTITUCIONES, SEPARADOS POR UNA COMA\n").split(",")
    
    pasantia = [] # Lista para guardar los datos de la pasantía
    trabajos = [] # Lista para guardar los datos de los trabajos

    while True: # Bucle para repetir el proceso hasta que el usuario escriba 'N o n'
        opcion = input("QUIERES REGISTRAR UNA PASANTIA - S/N: ")
        if opcion == "S" or opcion == "s":
            duracion = input("DURACION DE LA PASANTIA\n")
            lugar = input("LUGAR DE LA PASANTIA: \n")
            cargo = input("CARGO EN LA PASANTIA: \n ")
            pasantia.append({"duracion": duracion, "lugar": lugar, "cargo": cargo}) # Se agrega un diccionario con los datos de la pasantía a la lista
        elif opcion == "N" or opcion == "n": # Si el usuario escribe 'N', se sale del bucle
            break
    while True: # Bucle para repetir el proceso hasta que el usuario escriba 'n o N'
        opcion = input("QUIERES REGISTRAR UN TRABAJO - S/N: ")
        if opcion == "S" or opcion == "s":
            modalidad = input("INGRESE MODALIDAD DEL TRABAJO ")
            actividad = input("INGRESAR ACTIVIDAD DEL TRABAJO ")
            fecha = input("INGRESAR FECHA DEL TRABAJO ")
            trabajos.append({"modalidad": modalidad, "actividad": actividad, "fecha": fecha}) # Se agrega un diccionario con los datos del trabajo a la lista
        elif opcion == "N" or opcion == "n": # Si el usuario escribe 'n o N', se sale del bucle
            break

        
    habilidades = input("HABILIDADES, SEPARADOS POR UNA COMA\n").split(",")
    intereses = input("INTERESES, SEPARADOS POR UNA COMA\n").split(",")

    # Crear un diccionario con la estructura "laboral" y los valores de las listas

    #  PREPARA LA ESTRUCTURA JSON CON LOS DATOS INGRESAROR PARA INSERTARLO EN LA BD
    documento = {}
    documento["resumen"] = resumen
    documento["datos_personales"] = {}
    documento["datos_personales"]["nombre"] = nombre
    documento["datos_personales"]["apellido"] = apellido
    documento["direccion"] = {}
    documento["direccion"]["pais"] = pais
    documento["direccion"]["estado"] = estado
    documento["direccion"]["ciudad"] = ciudad
    documento["direccion"]["residencia"] = residencia

    documento["telefono"] = telefonos
    documento["email"] = email
    documento["redes"] = {}
    documento["redes"]["facebook"] = facebook
    documento["redes"]["instagram"] = instagram
    documento["redes"]["github"] = github

    documento["educacion"] = {}
    documento["educacion"]["nivel"] = nivel
    documento["educacion"]["titulo"] = titulos
    documento["educacion"]["institucion"] = instituciones

    documento["laboral"] = {}
    documento["laboral"]["pasantia"] = pasantia
    documento["laboral"]["pasantia"] = trabajos

    documento["habilidades"] = habilidades
    documento["intereses"] = intereses

    ingresarCV(documento)

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
                solicitarDatosCV()
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
