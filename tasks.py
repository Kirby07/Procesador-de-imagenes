from celery import current_app as app

from PIL import Image


@app.task

def resize_image(image_path, output_path, size):

    """Redimensiona una imagen a un tamaño especificado."""

    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(output_path)