import os
from datetime import datetime
import hashlib
import json
from pathlib import Path


from pelican import signals

# Function extracted from https://stackoverflow.com/a/19308592/7690767
def get_filepaths(directory, extensions=None, ignores=None):
        """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        file_paths = []  # List which will store all of the full filepaths.

        if extensions is None:
            extensions = []

        exts = extensions

        if isinstance(extensions, str):
            exts = [extensions]

        if ignores is None:
            ignores = []

        igns = ignores

        if isinstance(ignores, str):
            igns = [ignores]

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:

                if filename in igns or not any(filename.endswith(f".{ext}") for ext in exts):
                    continue

                filepath = os.path.join(root, filename).replace("\\", "/")
                file_paths.append(filepath)

        return file_paths

def create_service_worker(sender):

    output_path = sender.settings.get('OUTPUT_PATH', None) # carpeta donde se va a guardar el sitio
    sw_template = sender.settings.get('SERVICE_WORKER_THEMPLATE', None) # plantilla

    if None in [output_path, sw_template]: # cortar ejecución en caso de ser None
        return
    # preguntar por las siguientes extensiones, archivos que se guardarán en la caché
    extensions = ['js', 'html', 'css', 'svg', 'ini', 'ico', 'webmanifest', 'xml'] # archivos de texto
    img_extensions = ['png', 'jpg', 'gif'] # extensiones de las imágenes
    ignores = ['sw.js'] # archivo a ignorar, archivo de salida ya actualizado para evitar bucle de guardarse a sí mimos el Service Worker

    FILES = get_filepaths(output_path, extensions, ignores=ignores) # buscar los archivos en el árbol de directorio

    images = get_filepaths(output_path, img_extensions, ignores=ignores) # agregar las imágenes pero las modificará pero sólo agregará a la lista las imágenes de extensión -thumbnail en su nombre

    thumbnails = [filename for filename in images if '-thumbnail' in filename] # en caso de no ser así la lista estará vacía y no arrajará ningún error.

    FILES.extend(thumbnails) # concatenar ambas listas

    files_to_cache = []

    for filename in FILES:

        if filename.endswith('index.html'):
            filename_without_index = filename[:-10]
            files_to_cache.append(filename_without_index)

        files_to_cache.append(filename)

    # Remove output folder from path - Compatible with CI
    files_to_cache = [path.split(Path(output_path).stem)[-1] for path in files_to_cache]

    # Special case for /
    files_to_cache.append('/') # raíz del archivo

    FILES_TO_CACHE = sorted(set(files_to_cache))

    # leer el archivo y guardarlo en content.
    # leer la plantilla
    with open(sw_template, 'r+') as template_file:
        contents = template_file.read()

    # se realizan dos modificaciones en la plantilla
    files_to_cache_json = json.dumps(FILES_TO_CACHE, sort_keys=True, indent=4)
    # 1ra modificación
    contents = contents.replace('"$FILES_TO_CACHE$"', files_to_cache_json)

    version = str(datetime.now())
    version_hash = hashlib.md5(version.encode('utf-8')).hexdigest()[-7:]
    # 2da modificación
    contents = contents.replace('$VERSION$', version_hash)

    with open(f'{output_path}/sw.js','w') as output_file:
        # guardar versión modificada con un nuevo nombre en otro lugar. en el directorio de salida.
        output_file.write(contents)
# al final cuando pelican haya terminado su ejecución para poder crear el Service Worker de manera adecuada.
def register():
    signals.finalized.connect(create_service_worker)
