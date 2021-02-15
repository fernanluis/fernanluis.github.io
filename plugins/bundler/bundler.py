import os
from pathlib import Path
from pelican import signals

# Function extracted from https://stackoverflow.com/a/19308592/7690767
# Las tres funciones que le dan toda la funcionalidad al plugin
def get_filepaths(directory, extensions=[], ignores=[]): # ignore es una lista de archivo que se deben ignorar
    file_paths = []  # List which will store all of the full filepaths.

    exts = extensions

    if isinstance(extensions, str):
        exts = [extensions]

    igns = ignores

    if isinstance(ignores, str):
        igns = [ignores]

    # Walk the tree , de manera recursiva
    for root, directories, files in os.walk(directory):
        for filename in files:

            if filename in igns or not any(filename.endswith(f".{ext}") for ext in exts):
                continue

            filepath = Path(root, filename)
            file_paths.append(filepath)

    return file_paths

# dos archivos, el destino y cada uno de las lista.
def create_bundle(files, output):
    with open(output, 'w') as outfile: # abrir el archivo destino y sobreescribir si existe y si no lo crea
        for fname in files:
            with open(fname) as infile: # para cada uno delos archivos
                outfile.write('\n\n') # dos líneas en blanco
                for line in infile:
                    outfile.write(line)

# función a la que se suscribe
def create_bundles(sender):
    theme_path = sender.settings.get('THEME', None) # leer la variable donde está alojado el tema

    if theme_path is None: # se espera que no sea None sino termina la ejecución
        return
    # creación de paquetes independientes, comportamiento del sitio y la parte estética del sitio
    js_bundle = f'{theme_path}/static/js/scripts_bundled.js' # variable de archivo destino
    js_filenames = get_filepaths(theme_path, 'js', "scripts_bundled.js")# conseguir listado de las rutas que son archivos JavaScript
    create_bundle(js_filenames, js_bundle) # concatenación y sobreescritura

    css_bundle = f'{theme_path}/static/css/style_bundled.css' # variable de archivo destino
    css_filenames = get_filepaths(theme_path, 'css', "style_bundled.css")# conseguir listado de las rutas que son archivos css
    create_bundle(css_filenames, css_bundle)


# suscripción de pelican initialized aunque los archivos CSS y JavaScript serán empaquetados, esto en realidad, se podría hacer al inicio o al final
def register():
    signals.initialized.connect(create_bundles)
