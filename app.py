from pymongo import MongoClient
import json
from bson import ObjectId
import bson.errors
import time


#----------------------------------------Datos de conexión a MongoDB Atlas
MONGO_USERNAME = ''  # Cambiar por el usuario creado en Mongodb Atlas 
MONGO_PASSWORD = ''       # Cambiar por la contraseña de el usuario creado
MONGO_CLUSTER_ADDRESS = 'proyectocurriculumsdb.o0yltik.mongodb.net'
MONGO_URI = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_ADDRESS}/cv?retryWrites=true&w=majority'
DB_NAME = 'cv'
COLLECTION_NAME = 'curriculums'
#----------------------------------------Datos de conexión a MongoDB Atlas


#----------------------------------------Conexión de Base de Datos
def connect_to_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection
#----------------------------------------Conexión de Base de Datos


#----------------------------------------Insertar CVs a la Base de Datos
def insert_data(collection):
    # Cargar datos existentes desde la base de datos
    existing_data = collection.find({}, {"datos_personales.cedula": 1, "_id": 0})
    existing_cedulas = set(cv["datos_personales"]["cedula"] for cv in existing_data)

    # Leer los currículums desde el archivo JSON
    with open('cv.json', 'r') as file:
        curriculums_data = json.load(file)

    # Filtrar los currículums que no están en la base de datos por cédula
    new_curriculums = [cv for cv in curriculums_data if "datos_personales" in cv and "cedula" in cv["datos_personales"] and cv["datos_personales"]["cedula"] not in existing_cedulas]

    # Insertar los currículums filtrados en la base de datos
    if new_curriculums:
        collection.insert_many(new_curriculums)
#----------------------------------------Insertar CVs a la Base de Datos
        

#----------------------------------------Imprimir todos los Cvs existentes en la Base de Datos
def imprimir_todos_los_cv(collection):
    print("\n== Todos los Currículums ==")
    
    cursor = collection.find()

    for curr in cursor:
        print("\nCurrículum:")
        print(f"ID: {curr['_id']}")
        
        # Imprimir todos los campos del currículum
        print("Resumen:", curr.get("resumen"))

        datos_personales = curr.get("datos_personales", {})
        print("Datos Personales:")
        print(f"  Cedula: {datos_personales.get('cedula')}")
        print(f"  Nombre: {datos_personales.get('nombre')}")
        print(f"  Apellido: {datos_personales.get('apellido')}")

        direccion = curr.get("direccion", {})
        print("Direccion:")
        print(f"  Pais: {direccion.get('pais')}")
        print(f"  Estado: {direccion.get('estado')}")
        print(f"  Ciudad: {direccion.get('ciudad')}")
        print(f"  Residencia: {direccion.get('residencia')}")

        print("Telefono:", curr.get("telefono", []))
        print("Email:", curr.get("email"))

        redes = curr.get("redes", {})
        print("Redes:")
        print(f"  Facebook: {redes.get('facebook')}")
        print(f"  Instagram: {redes.get('instagram')}")
        print(f"  Github: {redes.get('github')}")

        educacion = curr.get("educacion", {})
        print("Educacion:")
        print(f"  Nivel: {educacion.get('nivel')}")
        print(f"  Titulos: {', '.join(educacion.get('titulo', []))}")
        print(f"  Instituciones: {', '.join(educacion.get('institucion', []))}")

        laboral = curr.get("laboral", {})
        print("Laboral:")
        print("  Pasantias:")
        for pasantia in laboral.get("pasantia", []):
            print(f"    Duracion: {pasantia.get('duracion')}, Lugar: {pasantia.get('lugar')}, Cargo: {pasantia.get('cargo')}")

        print("  Trabajos:")
        for trabajo in laboral.get("trabajos", []):
            print(f"    Modalidad: {trabajo.get('modalidad')}, Actividad: {trabajo.get('actividad')}, Fecha: {trabajo.get('fecha')}")

        print("Habilidades:", ', '.join(curr.get("habilidades", [])))
        print("Intereses:", ', '.join(curr.get("intereses", [])))

        print("\n-----------------------------")

    print("Fin de la lista de currículums.\n")
#----------------------------------------Imprimir todos los Cvs existentes en la Base de Datos


#----------------------------------------Solicitar datos del CV
def solicitarDatosCV():

    try:
        with open("cv.json", "r") as archivo:
            cvs_existentes = json.load(archivo)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        cvs_existentes = []

    # Solicitar la cédula
    cedula = input("CEDULA\n")

    # Verificar si la cédula ya existe
    for cv in cvs_existentes:
        if "datos_personales" in cv and "cedula" in cv["datos_personales"] and cv["datos_personales"]["cedula"] == cedula:
            print("Error: Esta cédula ya existe. No se puede guardar el CV.")
            return

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
        try:
            if opcion == "S" or opcion == "s":
                duracion = input("DURACION DE LA PASANTIA\n")
                lugar = input("LUGAR DE LA PASANTIA: \n")
                cargo = input("CARGO EN LA PASANTIA: \n ")
                pasantia.append({"duracion": duracion, "lugar": lugar, "cargo": cargo}) # Se agrega un diccionario con los datos de la pasantía a la lista
            elif opcion == "N" or opcion == "n": # Si el usuario escribe 'N', se sale del bucle
                break
        except ValueError:
            print("INGRESE UNA OPCION VALIDA\n")

    while True: # Bucle para repetir el proceso hasta que el usuario escriba 'n o N'
        opcion = input("QUIERES REGISTRAR UN TRABAJO - S/N: ")
        try:
            if opcion == "S" or opcion == "s":
                modalidad = input("INGRESE MODALIDAD DEL TRABAJO ")
                actividad = input("INGRESAR ACTIVIDAD DEL TRABAJO ")
                fecha = input("INGRESAR FECHA DEL TRABAJO ")
                trabajos.append({"modalidad": modalidad, "actividad": actividad, "fecha": fecha}) # Se agrega un diccionario con los datos del trabajo a la lista
            elif opcion == "N" or opcion == "n": # Si el usuario escribe 'n o N', se sale del bucle
                break
        except ValueError:
            print("INGRESE UNA OPCION VALIDA\n")
        
    habilidades = input("HABILIDADES, SEPARADOS POR UNA COMA\n").split(",")
    intereses = input("INTERESES, SEPARADOS POR UNA COMA\n").split(",")

    # Crear un diccionario con la estructura "laboral" y los valores de las listas

    #  PREPARA LA ESTRUCTURA JSON CON LOS DATOS INGRESAROR PARA INSERTARLO EN LA BD
    documento = {}
    documento["resumen"] = resumen
    documento["datos_personales"] = {}
    documento["datos_personales"]["cedula"] = cedula
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
    documento["laboral"]["trabajos"] = trabajos

    documento["habilidades"] = habilidades
    documento["intereses"] = intereses

    # Agregar el nuevo CV a la lista de CV existentes
    cvs_existentes.append(documento)

    # Guardar todos los CV en el archivo
    with open("cv.json", "w") as archivo:
        json.dump(cvs_existentes, archivo, indent=2)
#----------------------------------------Solicitar datos del CV
        

#----------------------------------------Eliminar CV por cédula
def eliminar_cv_por_cedula(collection):
    cedula_a_eliminar = input("\nIngrese la cédula del currículum a eliminar: ")

    try:
        with open("cv.json", "r") as archivo:
            cvs_existentes = json.load(archivo)

        # Verificar si la cédula existe y eliminar el currículum correspondiente
        nuevo_json = []
        eliminado = False
        for cv in cvs_existentes:
            if "datos_personales" in cv and "cedula" in cv["datos_personales"] and cv["datos_personales"]["cedula"] == cedula_a_eliminar:
                print(f"Se eliminó correctamente el currículum con cédula {cedula_a_eliminar}")
                eliminado = True
            else:
                nuevo_json.append(cv)

        if not eliminado:
            print(f"No se encontró ningún currículum con la cédula {cedula_a_eliminar}")

        # Guardar los currículums restantes en el archivo
        with open("cv.json", "w") as archivo:
            json.dump(nuevo_json, archivo, indent=2)

    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("Error al leer el archivo de currículums.")
    
    # Eliminar curriculums de la Base de Datos
    collection.delete_many({})
#----------------------------------------Eliminar CV por cédula


#----------------------------------------Imprimir un CV por cedula
def imprimir_curriculum_por_cedula(collection):
    cedula_a_buscar = input("\nIngrese la cédula del currículum a imprimir: ")

    # Buscar el currículum con la cédula especificada
    curr = collection.find_one({"datos_personales.cedula": cedula_a_buscar})

    if curr:
        print("\nCurrículum:")
        print(f"ID: {curr['_id']}")

        # Imprimir todos los campos del currículum
        print("Resumen:", curr.get("resumen"))

        datos_personales = curr.get("datos_personales", {})
        print("Datos Personales:")
        print(f"  Cedula: {datos_personales.get('cedula')}")
        print(f"  Nombre: {datos_personales.get('nombre')}")
        print(f"  Apellido: {datos_personales.get('apellido')}")

        direccion = curr.get("direccion", {})
        print("Direccion:")
        print(f"  Pais: {direccion.get('pais')}")
        print(f"  Estado: {direccion.get('estado')}")
        print(f"  Ciudad: {direccion.get('ciudad')}")
        print(f"  Residencia: {direccion.get('residencia')}")

        print("Telefono:", curr.get("telefono", []))
        print("Email:", curr.get("email"))

        redes = curr.get("redes", {})
        print("Redes:")
        print(f"  Facebook: {redes.get('facebook')}")
        print(f"  Instagram: {redes.get('instagram')}")
        print(f"  Github: {redes.get('github')}")

        educacion = curr.get("educacion", {})
        print("Educacion:")
        print(f"  Nivel: {educacion.get('nivel')}")
        print(f"  Titulos: {', '.join(educacion.get('titulo', []))}")
        print(f"  Instituciones: {', '.join(educacion.get('institucion', []))}")

        laboral = curr.get("laboral", {})
        print("Laboral:")
        print("  Pasantias:")
        for pasantia in laboral.get("pasantia", []):
            print(f"    Duracion: {pasantia.get('duracion')}, Lugar: {pasantia.get('lugar')}, Cargo: {pasantia.get('cargo')}")

        print("  Trabajos:")
        for trabajo in laboral.get("trabajos", []):
            print(f"    Modalidad: {trabajo.get('modalidad')}, Actividad: {trabajo.get('actividad')}, Fecha: {trabajo.get('fecha')}")

        print("Habilidades:", ', '.join(curr.get("habilidades", [])))
        print("Intereses:", ', '.join(curr.get("intereses", [])))

        print("\n-----------------------------")
    else:
        print(f"No se encontró ningún currículum con la cédula {cedula_a_buscar}.")
#----------------------------------------Imprimir un CV por cedula
        

#----------------------------------------Funciones para modificar CV

#-----------------------------Modificar resumen en el Json
def modificar_resumen(curriculum):
    nuevo_resumen = input("\nIngrese el nuevo resumen: ")
    curriculum["resumen"] = nuevo_resumen
    print("Resumen modificado correctamente.")
#-----------------------------Modificar resumen en el Json


#-----------------------------Modificar Datos Personales en el Json
def modificar_datos_personales(curriculum):
    nuevo_nombre = input("\nIngrese el nuevo nombre: ")
    nuevo_apellido = input("Ingrese el nuevo apellido: ")

    # Actualizar los datos personales
    curriculum['datos_personales']['nombre'] = nuevo_nombre
    curriculum['datos_personales']['apellido'] = nuevo_apellido

    print("Datos personales modificados correctamente.")
#-----------------------------Modificar Datos Personales en el Json


#-----------------------------Modificar email en el Json
def modificar_email(curriculum):
    
    nuevo_email = input("Ingrese el nuevo email: ")

    # Actualizar email
    curriculum["email"] = nuevo_email

    print("Email modificado correctamente.")
#-----------------------------Modificar email en el Json


#-----------------------------Modificar telefono en el Json
def modificar_telefono(curriculum):
    
    nuevo_telefono = input("\nIngrese el nuevo telefono: ")
    
    # Actualizar telefono
    curriculum["telefono"] = nuevo_telefono

    print("Telefono modificadoo correctamente.")
#-----------------------------Modificar telefono en el Json


#-----------------------------Modificar redes en el Json
def modificar_redes(curriculum):

    facebook = input("\nIngrese el nuevo Facebook: ")
    instagram = input("Ingrese el nuevo Instagram: ")
    github = input("Ingrese el nuevo GitHub: ")

    # Actualizar las redes sociales
    curriculum["redes"]["facebook"] = facebook
    curriculum["redes"]["instagram"] = instagram
    curriculum["redes"]["github"] = github

    print("Redes modificadas correctamente.")
#-----------------------------Modificar redes en el Json


#-----------------------------Modificar los datos de educacion en el Json
def modificar_educacion(curriculum):
    
    nivel = input("Nivel de educación: ")
    titulos = input("Títulos obtenidos (separados por comas): ").split(", ")
    instituciones = input("Instituciones educativas (separadas por comas): ").split(", ")

    # Actualizar los datos de educacion
    curriculum["educacion"]["nivel"] = nivel
    curriculum["educacion"]["titulo"] = titulos
    curriculum["educacion"]["institucion"] = instituciones

    print("Datos de educación modificados correctamente.")
#-----------------------------Modificar los datos de educacion en el Json


#-----------------------------Agregar nuevos Datos de Trabajo en el Json
def modificarTrabajo(curriculum):
    print("\n== Añadir Laboral - Trabajo ==")
    modalidad = input("Ingrese Modalidad: ")
    actividad = input("Ingrese Actividad: ")
    fecha = input("Ingrese Fecha: ")
    nuevo_trabajo = {
        "modalidad": modalidad,
        "actividad": actividad,
        "fecha": fecha
    }

    # Verificar si existe la clave 'laboral' en el currículum
    if 'laboral' not in curriculum:
        curriculum['laboral'] = {}

    # Verificar si existe la clave 'trabajos' en laboral
    if 'trabajos' not in curriculum['laboral']:
        curriculum['laboral']['trabajos'] = []

    # Agregar el nuevo trabajo a la lista de trabajos
    curriculum['laboral']['trabajos'].append(nuevo_trabajo)

    print("Trabajo agregado correctamente.")
#-----------------------------Agregar nuevos Datos de Trabajo en el Json


#-----------------------------Agregar nuevos Datos de Pasantia en el Json
def modificarPasantia(curriculum):
    print("\n== Añadir Laboral - Pasantía ==")
    duracion = input("Ingrese Duración: ")
    lugar = input("Ingrese Lugar: ")
    cargo = input("Ingrese Cargo: ")
    nueva_pasantia = {
        "duracion": duracion,
        "lugar": lugar,
        "cargo": cargo
    }

    # Verificar si existe la clave 'laboral' en el currículum
    if 'laboral' not in curriculum:
        curriculum['laboral'] = {}

    # Verificar si existe la clave 'pasantia' en laboral
    if 'pasantia' not in curriculum['laboral']:
        curriculum['laboral']['pasantia'] = []

    # Agregar la nueva pasantía a la lista de pasantías
    curriculum['laboral']['pasantia'].append(nueva_pasantia)

    print("Pasantía agregada correctamente.")
#-----------------------------Agregar nuevos Datos de Pasantia en el Json


#-----------------------------Menu para modificar Trabajos y Pasantias
def modificarLaboral(curriculum):
    print("\n== Añadir ==")
    print("1. Trabajo")
    print("2. Pasantia\n")
    print("=========================")
    opcion = int(input("Ingrese opción => "))
    try:
        if opcion == 1:
            modificarTrabajo(curriculum)
        elif opcion == 2:
            modificarPasantia(curriculum)
        else:
            print("Opcion no valida\n")
    except ValueError:
            print("Ingrese una opcion valida\n")
#-----------------------------Menu para modificar Trabajos y Pasantias


#-----------------------------Modificar Habilidades en el Json
def modificarHabilidades(curriculum):
    print("\n== Modificar Habilidades ==")
    habilidades_input = input("Ingreselas nuevamente separadas por una coma: ")
    
    # Verificar si se ingresaron habilidades
    if habilidades_input.strip():
        habilidades = habilidades_input.split(",")
        
        # Verificar si existe la clave 'habilidades' en el currículum
        if 'habilidades' not in curriculum:
            curriculum['habilidades'] = []

        # Reemplazar las habilidades existentes con las nuevas
        curriculum['habilidades'] = habilidades

        print("Habilidades modificadas correctamente.")
    else:
        print("No se ingresaron habilidades.")
#-----------------------------Modificar Habilidades en el Json


#-----------------------------Modificar Intereses en el Json
def modificarIntereses(curriculum):
    print("\n== Modificar Intereses ==")
    intereses_input = input("Ingréselos nuevamente separados por una coma: ")

    # Verificar si se ingresaron intereses
    if intereses_input.strip():
        intereses = intereses_input.split(",")

        # Verificar si existe la clave 'intereses' en el currículum
        if 'intereses' not in curriculum:
            curriculum['intereses'] = []

        # Reemplazar los intereses existentes con los nuevos
        curriculum['intereses'] = intereses

        print("Intereses modificados correctamente.")
    else:
        print("No se ingresaron intereses.")
#-----------------------------Modificar Intereses en el Json


#-----------------------------Menu para modificar los datos del Json
def menuModificacion(curriculum):

    while True:
        print("\n== Menu para Modificación de Datos del CV ==")
        print("Seleccione una opción:")
        print("1. Modificar el Resumen")
        print("2. Modificar Datos Personales")
        print("3. Modificar Email")
        print("4. Modificar Telefono")
        print("5. Modificar Redes Sociales")
        print("6. Modificar el Datos de Educación")
        print("7. Modificar Datos Laborales")
        print("8. Modificar Datos de Habilidades")
        print("9. Modificar Datos de Intereses")
        print("0. Realizar Cambios - (Volver al Menu Principal)")
        print("=========================")
        opcion = int(input("Ingrese opción => "))

        try:
            if opcion == 1:
                modificar_resumen(curriculum)
            elif opcion == 2:
                modificar_datos_personales(curriculum)
            elif opcion == 3:
                modificar_email(curriculum)
            elif opcion == 4:
                modificar_telefono(curriculum)
            elif opcion == 5: 
                modificar_redes(curriculum)
            elif opcion == 6:
                modificar_educacion(curriculum)
            elif opcion == 7:
                modificarLaboral(curriculum)
            elif opcion == 8:
                modificarHabilidades(curriculum)
            elif opcion == 0:
                return
            else:
                print("Opcion no valida\n")
                time.sleep(2)
        except ValueError:
            print("Ingrese una opcion valida\n")
#-----------------------------Menu para modificar los datos del Json


#-----------------------------Modificar la información de un CV por cédula
def modificar_curriculum_por_cedula():
    cedula_a_modificar = input("\nIngrese la cédula del currículum a modificar: ")

    try:
        with open("cv.json", "r") as archivo:
            cvs_existentes = json.load(archivo)

        # Buscar el currículum con la cédula especificada
        encontrado = False
        for cv in cvs_existentes:
            if "datos_personales" in cv and "cedula" in cv["datos_personales"] and cv["datos_personales"]["cedula"] == cedula_a_modificar:
                menuModificacion(cv)
                encontrado = True
                break

        if encontrado:
            # Guardar los currículums actualizados en el archivo
            with open("cv.json", "w") as archivo:
                json.dump(cvs_existentes, archivo, indent=2)

            # Buscar el currículum en MongoDB
            curriculum_en_bd = collection.find_one({"datos_personales.cedula": cedula_a_modificar})

            if curriculum_en_bd:
                # Actualizar el currículum en la colección
                collection.replace_one({"datos_personales.cedula": cedula_a_modificar}, cv)

                print(f"\nSe modificó correctamente el currículum con cédula {cedula_a_modificar} en el archivo JSON y en la colección de MongoDB.")
            else:
                print(f"No se encontró el currículum con cédula {cedula_a_modificar} en la base de datos.")
        else:
            print(f"\nNo se encontró ningún currículum con la cédula {cedula_a_modificar}.")

    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("Error al leer el archivo de currículums.")
    except Exception as e:
        print(f"Error al modificar el currículum en MongoDB: {str(e)}")
#-----------------------------Modificar la información de un CV por cédula

#----------------------------------------Funciones para modificar CV


#----------------------------------------Consultar las herramientas(habilidades) de cada individuo
def consultar_herramientas_por_individuo(collection):
    print("\n== Herramientas de los Currículums ==")
    
    # Obtener todos los currículums
    curriculums = collection.find()

    # Iterar sobre cada currículum
    for curriculum in curriculums:
        cedula = curriculum.get("datos_personales", {}).get("cedula")
        herramientas = curriculum.get("habilidades", [])

        # Contar la cantidad de herramientas manejadas
        cantidad_herramientas = len(herramientas)

        # Imprimir la información
        print(f"\nCédula: {cedula}")
        print(f"Herramientas: {', '.join(herramientas)}")
        print(f"Cantidad de Herramientas: {cantidad_herramientas}")
    
    print("\nFin de la lista de currículums.\n")
#----------------------------------------Consultar las herramientas(habilidades) de cada individuo


#----------------------------------------Opciones del menú
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
#----------------------------------------Opciones del menú


#----------------------------------------Conexion con la Base de Datos
collection = connect_to_mongodb()
#----------------------------------------Conexion con la Base de Datos


#----------------------------------------Programa principal
def main():

    while True:

        # Insertar datos al inicio del programa (solo si no se han insertado antes)
        insert_data(collection)

        # Mostrar opciones
        show_menu()

        try:
            opcion = int(input("Ingrese opción => "))
            if opcion == 1:
                solicitarDatosCV()
            elif opcion == 2:
                modificar_curriculum_por_cedula()
            elif opcion == 3:
                eliminar_cv_por_cedula(collection)
            elif opcion == 4:
                imprimir_curriculum_por_cedula(collection)
            elif opcion == 5:
                imprimir_todos_los_cv(collection)
            elif opcion == 6:
                print("opcion 6")
            elif opcion == 7:
                consultar_herramientas_por_individuo(collection)
            elif opcion == 8:
                print("opcion 1")
            elif opcion == 9:
                print("Saliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, elija una opción válida.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
#----------------------------------------Programa principal


#Main
if __name__ == "__main__":
    main()
