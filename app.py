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
    
def ingresarCV(documento):
    # INSERTA EN LA BD LOS DATOS PREPARADOS CON LA INFORMACION REGISTRADA POR EL USUARIO
    resultado = collection.insert_one(documento)
    verificarInsercion(resultado)

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

#FUNCIONES PARA REALIZAR MODIFICACIONES EN LOS DATOS DE LOS CV

# VERIFICA SI LA INSERCION DE UN DOCUMENTO FUE EXITOSA O NO

def verificarInsercion(resultado):
    if resultado.acknowledged:
        print("INSERCION EXITOSA, BAJO EL ID : ",resultado.inserted_id,"\n")
        return True
    else:
        print("LA INSERCION NO FUE EXITOSA \n")
        return False

#MUESTRA EN PANTALLA NOMBRE Y RESUMEN DE CV DE CADA PERSONA
def mostrarNombresResumen():
    results = collection.find()
    for indice, variable in enumerate(results):
        resumen = variable["resumen"]
        nombre = variable["datos_personales"]["nombre"]
        apellido = variable["datos_personales"]["apellido"]
        print("---------------------------------------------------------------------------------------------------------------------------------------------")
        print("\t {}-NOMBRE : {} {} ".format(indice+1,nombre,apellido))
        print("RESUMEN CURRICULAR {} ".format(resumen))
    
    print("---------------------------------------------------------------------------------------------------------------------------------------------")

#BUSCA UN ID DE DATO A INDICE INDICADO POR PARAMETRO
def buscarId(indice):
    results = collection.find()
    id = ""
    for iterador, variable in enumerate(results):
        if indice == iterador:
            id = variable["_id"]
    if id == "":
        print(" NO SE ENCONTRO EL ID DEL INDICE {} \n".format(indice))
    else:
        return id

#DEVUELVE EL INDICE QUE EL USUARIO HAYA MARCADO
def buscarIndice():
    results = collection.find()
    id = False
    for indice, variable in enumerate(results):
        resumen = variable["resumen"]
        nombre = variable["datos_personales"]["nombre"]
        apellido = variable["datos_personales"]["apellido"]
        print("---------------------------------------------------------------------------------------------------------------------------------------------")
        print("\t {}-NOMBRE : {} {} ".format(indice+1,nombre,apellido))
        print("RESUMEN CURRICULAR {} ".format(resumen))
    
    print("---------------------------------------------------------------------------------------------------------------------------------------------")
    indice = int(input("\tCUAL CURRICULUM DESEA MODIFICAR \n"))
    indice = indice - 1

    return indice    

#SOLICITA LOS DATOS PERSONALES QUE SERA MODIFICADOS

def modificacionDeDatosPersonales(id):
    result = collection.find_one({"_id":id})

    nombre = pedirNombre()
    modificarNombre(id,nombre)
    apellido = pedirApellido()
    modificarApellido(id,apellido)

    documentoDireccion = pedirDatosDireccion()
    modificarDireccion(id,documentoDireccion)

    print("MODIFICACION DE TELEFONO \n")
    print("1 MODIFICACION DE TELEFONO \n")
    print("2 AGREGAR UN NUEVO TELEFONO \n")
    option = int(input())

    try:
        if option == 1:
            indice = buscarIndiceTelefono(id)
            nuevoTelefono = pedirTelefono()
            modificarTelefono(id,indice,nuevoTelefono)
        if option == 2:
            nuevoTelefono = input("INGRESE EL NUMERO A AGREGAR\n")
            agregarTelefono(id,nuevoTelefono)
    except ValueError:
        print("INGRESE UNA OPCION VALIDA\n")

    email = pedirEmail()
    modificarEmail(id,email)

    documentoRedes = pedirRedes()
    modificarRedes(id,documentoRedes)

#EJECUTA EL QUERY PARA REALIZAR LOS CAMBIOS DE REDES EN LOS CV

def modificarRedes(id,redes):
    filtro = {"_id":id}
    operacion = {"$set":{"datos_personales.redes": redes}}
    resultado = collection.update_one(filtro,operacion)
    verificarActualizacion(resultado,"MODIFICACION DE REDES")

#EJECUTA EL QUERY PARA REALIZAR LOS CAMBIOS DE EMAIL EN LOS CV

def modificarEmail(id,nuevoEmail):
    filtro = {"_id":id}
    modificacion = {"$set":{"datos_personales.email":nuevoEmail}}
    resultado = collection.update_one(filtro,modificacion)
    verificarActualizacion(resultado,"MODIFICACION DE EMAIL")

#SOLICITA LAS REDES PARA INGRESARLAS EN LA BD

def pedirRedes():
    facebook = input("INGRESAR USUARIO FACEBOOK\n")
    instagram = input("INGRESAR USUARIO INSTAGRAM\n")
    github = input("INGRESAR USUARIO GITHUB\n")
    
    documentoRedes = {
        "facebook":facebook,
        "instagram":instagram,
        "github":github
    }
    return documentoRedes

#SOLICITA EL EMAIL POR PATALLA Y LO RETORNA

def pedirEmail():
    email = input("INGRESE EL NUEVO EMAIL\n")
    return email

#MODIFICA UN TELFONO YA EXISTENTE DENTRO DE LA BD

def modificarTelefono(id,indice,telefono):
    filtro = {"_id" :id,f"datos_personales.telefono.{indice}": {"$exists": True}}
    operacion = {"$set": {f"datos_personales.telefono.{indice}": telefono}}
    verificarActualizacion(collection.update_one(filtro, operacion),"TELFONO MODIFICADO")

#AGREGA UN NUEVO TELEFONO A LA COLECCION 

def agregarTelefono(id,telefono):
    filtro = {"_id" :id}
    operacion = {"$push": {"datos_personales.telefono": telefono}}
    verificarActualizacion(collection.update_one(filtro, operacion),"TELEFONO AGREGADO")

#SOLICITA POR PANTALLA AL USUARIO QUE INGRESE EL NUEVO TELEFONO

def pedirTelefono():
    telefono = input("INGRESE EL NUEVO TELEFONO\n")
    return telefono

#BUSCA UN INDICE ESPECIFICO DENTRO DEL ARRAY QUE ALMACENA LOS TELEFONOS EN LA BD

def buscarIndiceTelefono(id):
    filtro = {"_id":id}
    proyeccion = {"datos_personales.telefono": 1,"_id":0}
    result = collection.find_one(filtro,proyeccion)

    variable = result["datos_personales"]["telefono"]

    print("TELEFONOS REGISTRADOS \n")
    for iterador, telefono in enumerate(variable):
        print("{} - TELEFONO : {}".format(iterador+1,telefono))

    iterador = int(input("CUAL TELEFONO DESEA MODIFICAR \n"))

    if iterador < 0 or iterador > len(variable):
        print("ERROR NO SE ENCUENTRA ESE NUMERO\n")
        time.sleep(3)
    else:
        iterador = iterador - 1
        return iterador
    
#SOLICITA EL APELLIDO PARA SER MODIFICADO EN LA BD
def pedirApellido():
    apellido = input("NUEVO NOMBRE PARA EL CV - ESCRIBIR M o m PARA MANTENER EL ANTERIOR\n")
    return apellido

#SOLICITA EL NOMBRE PARA SER MODIFICADO EN LA BD

def pedirNombre():
    nombre = input("NUEVO NOMBRE PARA EL CV - ESCRIBIR M o m PARA MANTENER EL ANTERIOR\n")
    return nombre

#SOLICITA EL DATOS DE DIRECCION PARA SER MODIFICADO EN LA BD

def pedirDatosDireccion():
    print("MODIFCAR DATOS DE DIRECCION\n")
    pais = input("PAIS\n")
    estado = input("estado\n")
    ciudad = input("ciudad\n")
    residencia = input("residencia\n")

    documentoDireccion = {
        "pais": pais,
        "estado":estado,
        "ciudad": ciudad,
        "residencia": residencia
    }
    return documentoDireccion

#EJECUTA EL QUERY PARA MODIFICAR UN NOMBRE DE UN CV

def modificarNombre(id,nuevoNombre):
    if nuevoNombre == "m" or nuevoNombre == "M":
        return
    else:
        filtro = {"_id":id}
        modificacion = {"$set":{"datos_personales.nombre":nuevoNombre}}
        collection.update_one(filtro,modificacion)

#EJECUTA EL QUERY PARA MODIFICAR UN APELLIDO DE UN CV

def modificarApellido(id,nuevoApellido):
    if nuevoApellido == "m" or nuevoApellido == "M":
        return
    else:
        filtro = {"_id":id}
        modificacion = {"$set":{"datos_personales.apellido":nuevoApellido}}
        collection.update_one(filtro,modificacion)

#EJECUTA EL QUERY PARA MODIFICAR UNA DIRECCION DE UN CV

def modificarDireccion(id,documento):
    filtro = {"_id":id}
    operacion = {"$set":{"datos_personales.direccion": documento}}
    resultado = collection.update_one(filtro,operacion)
    verificarActualizacion(resultado,"MODIFICACION DIRECCION")

# VERIFICA QUE SI LA ULTIMA ACTUALIZACION FUE EJECUTA CON EXITO O NO
def verificarActualizacion(resultado,mensagge):
    if resultado.matched_count > 0 and resultado.modified_count > 0:
        print("ACTUALIZACION EXITOSA {} \n".format(mensagge))
        time.sleep(2)
        return True
    else:
        print("ACTUALIZACION HA FALLADO {} \n".format(mensagge))
        time.sleep(2)
        return False

# SOLICITA LOS DATOS PARA MODIFICAR EL RESUMEN Y LOS MODIFICA


def modificacionDeResumen(id):
    resumen = input(("INGRESE EL NUEVO RESUMEN CURRICULAR\n"))
    filtro = {"_id":id}
    proyeccion = {"$set":{"resumen":resumen}}
    resultado = collection.update_one(filtro,proyeccion)
    verificarActualizacion(resultado,"ACTUALIZACION DE RESUMEN")

# SOLICITA LOS DATOS PARA MODIFICAR LOS DATOS DE EDUCACION Y LOS MODIFICA

def modificacionEducacion(id):
    nivel = input("INGRESAR NIVEL DE EDUDACION\n")
    titulo = input("TITULO QUE DESEA AGREGAR SEPARAR CON COMA , SI SON VARIAS\n").split(",")
    instituciones = input("UNIVERSIDAD QUE DESEA AGREGAR CON COMA , SI SON VARIAS\n").split(",")

    filtro = {"_id":id}
    proyeccion = {"$set":{"educacion.nivel":nivel}}
    verificarActualizacion(collection.update_one(filtro,proyeccion),"MODIFICACION DEL NIVEL DE ESTUDIO\n")

    proyeccion = {"$push":{"educacion.titulo":{"$each":titulo}}}
    verificarActualizacion(collection.update_one(filtro,proyeccion),"MODIFICACION DE TITULOS\n")

    proyeccion = {"$push":{"educacion.institucion":{"$each":instituciones}}}
    verificarActualizacion(collection.update_one(filtro,proyeccion),"MODIFICACION DE INSTITUCIONES\n")

#MODIFICA LOS DATOS LABORALES DE UN CV ESPECIFICO
    
def modificarLaboral(id):
    print("DESEA AÑADIR TRABAJO O PASANTIA")
    print("1- TRABAJO\n")
    print("2- PASANTIA\n")
    option = int(input())
    try:
        if option == 1:
            modificarTrajo(id)
        if option == 2:
            modificarPasantia(id)
        else:
            print("OPCION NO VALIDA\n")
    except ValueError:
            print("INGRESE UNA OPCION VALIDA\n")
        
#MODIFICA LOS DATOS LABORALES DE UN CV ESPECIFICO
def modificarTrajo(id):
    print("DATOS DEL TRABAJO\n")
    modalidad = input("MODALIDAD\n")
    actividad = input("ACTIVIDAD\n")
    fecha = input("FECHA\n")
    documentoTrabajo = {
        "modalidad": modalidad,
        "actividad": actividad,
        "fecha": fecha
    }
    filtro = {"_id":id}
    proyeccion = {"$push":{"laboral.trabajos":documentoTrabajo}}
    verificarActualizacion(collection.update_one(filtro,proyeccion),"ACTUALIZACION TRABAJO")

# REALIZA CAMBIOS EN LOS DATOS DE PASANTIA DE UN CV
    
def modificarPasantia(id):
    print("DATOS DE LA PASANTIA\n")
    duracion = input("DURACION\n")
    lugar = input("LUGAR\n")
    cargo = input("cargo\n")
    documentoPasantia = {
        "duracion":duracion,
        "lugar":lugar,
        "cargo":cargo
    }
    filtro = {"_id":id}
    proyeccion = {"$push":{"laboral.pasantia":documentoPasantia}}
    verificarActualizacion(collection.update_one(filtro,proyeccion),"ACTUALIZACION PASANTIA")

#DESPLIEGA EL MENU PARA MODIFICAR O AGREGAR UNA NUEVA HABILIDAD

def modificacionHabilidades(id):
    print("AGREGAR O MODIFICAR UNA HABILIDAD\n")
    option = int(input("1- MODIFICAR HABILIDAD\n 2-AGREGAR HABILIDAD\n"))
    try:
        if option == 1:
            indice = buscarIndiceHabilidad(id)
            habilidad = pedirHabilidad()
            actualizarHabilidad(id,indice,habilidad)
        if option == 2:
            habilidad = pedirHabilidad()
            agregarHabilidad(id,habilidad)
            return
        else:
            print("OPCION NO VALIDA\n")
    except ValueError:
            print("INGRESE UNA OPCION VALIDA\n")

#AGREGA UNA NUEVA HABILIDAD INDICADA EN EL PARAMETRO EN UN CV ESPECIFICADO POR ID

def agregarHabilidad(id,habilidad):
    filtro = {"_id" :id}
    operacion = {"$push": {"habilidades": habilidad}}
    verificarActualizacion(collection.update_one(filtro, operacion),"HABILIDAD AGREGADA")

#SOLICITA AL USUARIO QUE INGRESE EL NOMBRE DE UNA NUEVA HABILIDAD

def pedirHabilidad():
    habilidad = input("INGRESE LA HABILIDAD\n")
    return habilidad

# EJECUTA EL QUERY PARA MODIFICAR UNA HABILIDAD YA EXISTENTE

def actualizarHabilidad(id,indice,habilidad):
    filtro = {"_id" :id,f"habilidades.{indice}": {"$exists": True}}
    operacion = {"$set": {f"habilidades.{indice}": habilidad}}
    verificarActualizacion(collection.update_one(filtro, operacion),"HABILIDAD MODIFICADO")

# BUSCA UNA HABILIDAD ESPECIFICA Y RETORNA SU INDICE EN EL ARREGLO

def buscarIndiceHabilidad(id):
    filtro = {"_id":id}
    proyeccion = {"habilidades": 1,"_id":0}
    result = collection.find_one(filtro,proyeccion)

    variable = result["habilidades"]

    print("HABILIDADES REGISTRADOS \n")
    for iterador, habilidad in enumerate(variable):
        print("{} - habilidad : {}".format(iterador+1,habilidad))

    iterador = int(input("CUAL HABILIDAD DESEA MODIFICAR \n"))

    if iterador < 0 or iterador > len(variable):
        print("ERROR NO SE ENCUENTRA ESE NUMERO\n")
    else:
        iterador = iterador - 1
        return iterador


# DESPLIEGA UN MENU EN PANTALLA QUE OFRECE MODIFICARO AGREGAR UNA NUEVA HABILIDAD
    
def modificarIntereses(id):
    print("AGREGAR O MODIFICAR UNA INTERES\n")
    option = int(input("1- MODIFICAR INTERES\n 2-AGREGAR INTERES\n"))
    try:
        if option == 1:
            indice = buscarIndiceInteres(id)
            interes = pedirInteres()
            actualizarInteres(id,indice,interes)
        elif option == 2:
            interes = pedirInteres()
            agregarInteres(id,interes)
        else:
            print("OPCION NO VALIDA\n")
    except ValueError:
        print("INGRESE UNA OPCION VALIDA\n")

#AGREGA UN NUEVO INTERES QUE RECIDIDO POR PARAMETRO EN LA FUNCION, Y ES AGREGADO EN UN CV ESPECIFICADO POR ID

def agregarInteres(id,interes):
    filtro = {"_id" :id}
    operacion = {"$push": {"intereses": interes}}
    verificarActualizacion(collection.update_one(filtro, operacion),"INTERES AGREGADO")

# SOLICITA LOS INTERESES AL USUARIO Y LOS RETORNA
    
def pedirInteres():
    interes = input("INGRESE EL NUEVO INTERES\n")
    return interes

# INGRESA EN LA BASE DE DATOS UNA ACTUALIZACION DE ALGUN INTERES

def actualizarInteres(id,indice,interes):
    filtro = {"_id" :id,f"intereses.{indice}": {"$exists": True}}
    operacion = {"$set": {f"intereses.{indice}": interes}}
    verificarActualizacion(collection.update_one(filtro, operacion),"INTERES MODIFICADO")

#BUSCA EL INDICE DE UN INTERES ESPECIFICO DENTRO DE UN ARREGLO Y RETORNA SU POSICION

def buscarIndiceInteres(id):
    filtro = {"_id":id}
    proyeccion = {"intereses": 1,"_id":0}
    result = collection.find_one(filtro,proyeccion)

    variable = result["intereses"]

    print("INTERESES REGISTRADOS \n")
    for iterador, interes in enumerate(variable):
        print("{} - habilidad : {}".format(iterador+1,interes))

    iterador = int(input("CUAL INTERES DESEA MODIFICAR \n"))

    if iterador < 0 or iterador > len(variable):
        print("ERROR NO SE ENCUENTRA ESE NUMERO\n")
    else:
        iterador = iterador - 1
        return iterador

#DESPLIEGA EN PANTALLA UN MENU QUE OFRECE LAS DIFENTES OPCIONES PARA MODIFICAR UN CV

def menuModificacion():
    while True:
        print("\n\t\tMENU PARA MODIFICACION DE DATOS DEL CV\n")
        print("1-MODIFICAR EL RESUMEN\n")
        print("2-MODIFICAR DATOS PERSONALES\n")
        print("3-MODIFICAR EL DATOS DE EDUCACION\n")
        print("4-MODIFICAR DATOS LABORALES\n")
        print("5-MODIFICAR DATOS DE HABILIDADES\n")
        print("6-MODIFICAR DATOS DE INTERESES\n")
        print("0-SALIR DEL MENU MODIFICACION\n")
        option = int(input())

        try:
            if option == 1:
                modificacionDeResumen(mostrarLista())
            elif option == 2:
                modificacionDeDatosPersonales(mostrarLista())
            elif option == 3:
                modificacionEducacion(mostrarLista())
            elif option == 4:
                modificarLaboral(mostrarLista())
            elif option == 5: 
                modificacionHabilidades(mostrarLista())
            elif option == 6:
                modificarIntereses(mostrarLista())
            elif option == 0:
                return
            else:
                print("OPCION NO VALIDAD\n")
                time.sleep(2)
        except ValueError:
            print("INGRESE UNA OPCION VALIDA\n")

#MUESTRA UNA LISTA SIMPLE EN PANTALLA DE LOS NOMBRES DE CV Y SU RESUMEN CURRICULAR

def mostrarLista():
    indice = buscarIndice()
    id = buscarId(indice)
    return id

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
                menuModificacion()
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
