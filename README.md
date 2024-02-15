# Proyecto de Gestión de Currículums

## Descripción del Proyecto

Este proyecto consiste en un sistema de gestión de currículums (CV) que permite realizar diversas operaciones, como la inserción de nuevos CV, la modificación de información existente, la eliminación de CV por cédula, la impresión de CV por cédula, la visualización de todos los CV existentes, la consulta de intereses comunes entre los individuos, la consulta de herramientas (habilidades) de cada individuo, y la consulta de los trabajos realizados por cada individuo.

## Funcionalidades del Sistema

1. **Inserción de Datos:**
   - La función `solicitarDatosCV()` permite ingresar y almacenar nuevos currículums en un archivo JSON y en una base de datos MongoDB.

2. **Modificación de Datos:**
   - La función `modificar_curriculum_por_cedula()` facilita la modificación de la información de un CV existente, permitiendo actualizar diferentes secciones como resumen, datos personales, email, teléfono, redes sociales, educación, laboral, habilidades, e intereses.

3. **Eliminación de CV por Cédula:**
   - La función `eliminar_cv_por_cedula(collection)` elimina un CV tanto del archivo JSON como de la base de datos MongoDB, utilizando la cédula como identificador.

4. **Impresión de CV por Cédula:**
   - La función `imprimir_curriculum_por_cedula(collection)` imprime la información detallada de un CV específico, identificado por la cédula.

5. **Impresión de Todos los CV:**
   - La función `imprimir_todos_los_cv(collection)` muestra la información resumida de todos los CV almacenados en la base de datos MongoDB.

6. **Consulta de Intereses Comunes:**
   - La función `consultar_intereses_comunes(collection)` permite buscar currículums con intereses comunes a partir de un interés específico.

7. **Consulta de Herramientas por Individuo:**
   - La función `consultar_herramientas_por_individuo(collection)` muestra las habilidades (herramientas) de cada individuo junto con la cantidad total de habilidades.

8. **Consulta de Trabajos Realizados:**
   - La función `consultar_trabajos_realizados(collection)` presenta la información laboral de cada individuo, incluyendo los trabajos realizados.

9. **Modificación de Datos (Menú Interactivo):**
   - La función `menuModificacion(curriculum)` proporciona un menú interactivo para modificar diferentes secciones de la información de un CV.

## Uso del Programa

1. **Inicio del Programa:**
   - Al ejecutar el programa, se mostrará un menú principal con diversas opciones.

2. **Selección de Opciones:**
   - El usuario puede seleccionar las opciones del menú para realizar las operaciones deseadas, como ingresar nuevos CV, modificar información existente, consultar datos, etc.

3. **Inserción de Datos:**
   - Al seleccionar la opción de inserción de datos, el usuario puede ingresar la información de un nuevo CV, la cual se almacenará en un archivo JSON y en la base de datos MongoDB.

4. **Modificación de Datos:**
   - La opción de modificación permite actualizar la información de un CV existente, proporcionando un menú interactivo para seleccionar qué sección modificar.

5. **Eliminación de CV:**
   - Se puede eliminar un CV ingresando la cédula del individuo. La eliminación afecta tanto al archivo JSON como a la base de datos MongoDB.

6. **Consulta de Datos:**
   - Las opciones de consulta permiten ver información detallada o resumida de CV específicos o de todos los CV almacenados.

7. **Consulta de Intereses y Herramientas:**
   - Estas opciones ofrecen consultas específicas, como buscar intereses comunes entre individuos o visualizar las habilidades de cada persona.

8. **Consulta de Trabajos Realizados:**
   - Permite ver los trabajos realizados por cada individuo.

9. **Salir del Programa:**
   - El usuario puede seleccionar la opción para salir del programa cuando haya completado las operaciones deseadas.

## Requisitos

1. **Python:**
   - Se requiere tener Python instalado en el sistema.

2. **Librerías:**
   - Asegurarse de tener las librerías necesarias instaladas, como pymongo.

3. **Base de Datos MongoDB:**
   - Se necesita una instancia de MongoDB para almacenar los currículums.

## Configuración del Programa

1. **Conexión con MongoDB:**
   - Asegurarse de modificar la función `connect_to_mongodb()` con la información correcta de la conexión a la base de datos MongoDB.

2. **Ejecución del Programa:**
   - Ejecutar el script principal (`main.py`) para iniciar el programa.

## Requerimientos Mínimos

Los curriculums que maneja el sistema cuentan con lo siguiente:

- Un resumen que corresponda a un campo de texto. Ejemplo:
```json
"resumen": "Estudiante con enfoque en analisis de datos."
```
- Claves con múltiples valores. Ejemplo: La clave "telefono" tiene múltiples valores, que representan diferentes números de teléfono.
```json
"telefono": [
   "+52 33 1234-5678",
   "+52 33 8765-4321",
   "+52 33 9876-5432",
   "+52 33 5432-8765"
]
```
- Claves de documentos. Ejemplo: Bajo la sección "laboral" representa una clave de documentos, ya que contiene múltiples documentos (objetos) con diferentes claves y valores.
```json
"pasantia": [
   {
      "duracion": "6 meses",
      "lugar": "Tech Solutions",
      "cargo": "Asistente de Desarrollo"
   },
   {
      "duracion": "3 meses",
      "lugar": "Innovate Labs",
      "cargo": "Analista de Datos"
   },
   {
      "duracion": "4 meses",
      "lugar": "CodeCrafters",
      "cargo": "Pasante de QA"
   }
]
```
## Créditos

Desarrollado por Antonietta Palazzo, Kevin Herrera y Álvaro Aguinagalde.
