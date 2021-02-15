import os
from pathlib import Path
from pelican import signals
from PIL import Image, ImageFilter # importación de la librería pillow, pero como es un fork mantiene el nombre original y se importa image ImageFilter

# Function extracted from https://stackoverflow.com/a/19308592/7690767
def get_filepaths(directory, extensions=[], ignores=[]):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    exts = extensions

    if isinstance(extensions, str):
        exts = [extensions]

    igns = ignores

    if isinstance(ignores, str):
        igns = [ignores]

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:

            if filename in igns or not any(filename.endswith(f".{ext}") for ext in exts):
                continue

            filepath = Path(root, filename)
            file_paths.append(filepath)

    return file_paths

# solicitará un directorio a las cuales hay que generarle la minuatura con un parámetro adicional y opcional que es el radio para saber cuán desenfocado estará la imagen.
def generate_blur_thumbnails(sender):

    content_path = sender.settings.get('BLUR_PATH', None)
    blur_radius = sender.settings.get('BLUR_RADIUS', 2)

    if content_path is None:
        return

    imgs = get_filepaths(content_path, ['jpg', 'png'])
    # iteración de la lista de las imágenes obteniendo la extensión, y todos menos la extensión.
    for filename in imgs:
        extension = filename.suffix # la extensión se obtiene con la librería Path
        name_alone = filename.parent / filename.stem # todos los ancestros se obtienen con parent y el nombre del archivo sin incluir la extensión se obtiene con stem.

        if filename.stem.endswith('-thumbnail'): # preguntar si el nombre de la extensión termina en thumbnails ya que si es así no se volverá a genarar para evitar proceso recursos de las miniaturas de las miniaturas de las miniaturas
            continue
        # código de pillow donde se abre la imagen, se convierte a RGB que es el sistema de colores al que se está acostumbrado a ver. rojo verde y azul
        im = Image.open(filename)
        im = im.convert(mode="RGB")
        im.thumbnail([200, 200], Image.ANTIALIAS) # se crea la imagen reducida en tamaño pero no la cortará
        im.filter(ImageFilter.GaussianBlur(blur_radius)).save(f'{name_alone}-thumbnail{extension}', optimize=True) # desenfoque gaussiano, filtro con un radius

# conección a la señal initialized vinculando al función generate_blur_thumbnails
def register():
    signals.initialized.connect(generate_blur_thumbnails)
