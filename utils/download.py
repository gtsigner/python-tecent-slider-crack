import uuid
import requests
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

ACCEPTED_FILE_FORMATS = ("gif", "png", "jpeg")


def download_image_as(url, file_format, file_name=None):
    # TODO: Attempt to get format from end of url string.
    # Ensure the file format is lowercase.
    file_format = file_format.lower()
    # Ensure the file format doesnt starts with a period.
    if file_format.startswith("."):
        file_format = "".join(file_format.split(".")[1:])
    # Ensure the file format is one that we accept.
    if file_format not in ACCEPTED_FILE_FORMATS:
        raise Exception("Not an accepted format. ({})".format(file_format))
    # Ensure the url doesnt start with no protocol.
    if url.startswith('//'):
        url = 'http://' + url.split('//')[1]
    # Get the response data.
    response = requests.get(url)
    # If we failed to get a response, raise an exception.
    if response.status_code != 200:
        raise Exception("Failed to download image at url {} , code: {}".format(url, response.status_code))
    # Create a new copy of the image we downloaded in memory.
    infile = Image.open(BytesIO(response.content))
    if infile.mode != 'RGB':
        infile = infile.convert('RGB')
    infile.save(file_name)
    # Create a universal fileanme if we don't get one to use.
    return file_name, response.status_code


def download_image_as_gif(url, file_name=None):
    return download_image_as(url, "GIF", file_name)


def download_image_as_jpeg(url, file_name=None):
    return download_image_as(url, "JPEG", file_name)


def download_image_as_png(url, file_name=None):
    return download_image_as(url, "PNG", file_name)
