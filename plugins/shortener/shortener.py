# acortador de enlace crea una página de HTML con una etiqueta META refresh
# el refresh es la explicitar una URL
import os # biblioteca del sistma operativo
import json # librería json, nativa de la biblioteca estándar de python
from pathlib import Path # para trabar con rutas de directorio

from pelican import signals

# función la función generate_output quien se ejecutará cuando Pelican termine de generar el sitio.
# función con un emisor, un objeto de Pelican
def generate_output(sender): # sender es arbitrario
    output_path = sender.settings.get("OUTPUT_PATH", None) # leer desde pelicanconf o publishconf el archivo de configuración utilizado OUTPUT_PATH

    # también el archivo shortener que es desde dónde se estarán leyendo las URLs
    shortener_file = sender.settings.get('SHORTENER_FILE', None)
    # si la variables es None
    if shortener_file is None:
        print("No shortener File was given")
        return

    # en caso de que no sea None, es decir, en caso de que haya algún archivo, abrir el archivo y leerlo
    # asumiendo que es un archivo json
    with open(shortener_file) as file:
        redirects_map = json.load(file) # mapeo de redireccionamientos con clave valor desde:hacia
    # extraer una carpeta, encapsulando todos los links acortados dentro de una carpeta.
    redirects_folder = sender.settings.get('SHORTENER_FOLDER', None)

    # asegurar que la carpeta no sea None, por que si es así deberá utilizar la salida del directorio concatenando la salida con la carpeta nueva
    output_path_with_folder = output_path

    if redirects_folder is not None:
        output_path_with_folder = Path(output_path, redirects_folder) # la salida es /docs
# iterar para cada par del mapa de redirección; desde:hacia invocando la función de abajo con los siguientes datos.
    for filename, redirect_url in redirects_map.items():
        generate_folder_file(filename, output_path_with_folder, redirect_url)
    
# crear un carpeta que contenga index.html para que el navegador mostrará por defecto: deberá tener un archivo, el nombre de la carpeta y un enlace al cual se desea redireccionar.
def generate_folder_file(file, folder, link):
# definición de plantilla HTML necesaria
    BASE_HTML = """
    <html>
        <head>
            <meta http-equiv="refresh" content="0; URL='{0}'" />
        </head>
        <body>
        </body>
    </html>
    """
# si en enlace pasado como parámetro de la función no tiene un protocolo asociado fundamental para evitar errores.
    if not (link.startswith('http://') or link.startswith('https://')):
        link = 'http://' + link # si no lo tiene se agrega http
# luego, dentro de la biblioteca estándar crear una carpeta con el archivo concatenado con un path para facilitar interpretación de las rutas.
    folder_path = Path(folder, file)
# ahora debe asegurarse se que la carpeta exista, porque si existe no se podrá crear el archivo HTML dentro.
    os.makedirs(folder_path, exist_ok=True) # método makedirs que quiere decir: hacer directorios con el parámetro opcional exist_ok el cual no lanzará un error si este directorio existe
    # en el caso de ser múltiples directorios los creará todos de manera recursiva.
# agregar index.html al directorios
    file_path = Path(folder_path, 'index.html')
# escribir contenido HTML dentro del archivo abriendo el archivo en modo escritura y se escribe el archivo.
    with open(file_path, 'w', encoding='utf-8') as fd:
        content = BASE_HTML.format(link) # format para introducir la URL dentro la plantilla html
        fd.write(content) # escribir el contenido.

# iterar u obtener los enlaces importando las señales de Pelican y se escribirá el método register()
def register():
    signals.finalized.connect(generate_output) # señal finalized contectada
