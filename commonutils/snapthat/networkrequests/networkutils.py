import numpy as np
from PIL import Image
import base64
from io import BytesIO
import PIL
import requests
import traceback
import time
from flask import jsonify
from urllib.parse import urlparse



def string_to_base64(string):
    """convert a string to base64 number

    Args:
        string(str):  a string to be encoded to base64

    Returns:
        str: a base64 string

    """

    b = string.encode('utf-8')
    encoded_string = base64.b64encode(b)
    encoded_string = encoded_string.decode('utf-8')
    return encoded_string

def bytes_to_base64(byts):
    """convert a string to base64 number

    Args:
        string(str):  a string to be encoded to base64

    Returns:
        str: a base64 string

    """
    encoded_string = base64.b64encode(byts)
    encoded_string = encoded_string.decode('utf-8')
    return encoded_string

def base64_to_string(base64string):
    """decode  a base64 byte string

    Args:
        base64string(str): base64 byte string

    Returns:
        str: the original string

    """
    s = base64.b64decode(base64string)
    s = s.decode("utf-8")
    return s

def base64_to_bytes(base64string):
    """decode  a base64 byte string

    Args:
        base64string(str): base64 byte string

    Returns:
        bytes: the original byte content

    """
    s = base64.b64decode(base64string)
    return s


def base64_to_imagearray(base64string, image_size):
    """converts the base 64 image string to numpy array

    Args:
        base64string(str):
        image_size(list[int]): image size of format [IMAGE_WIDTH, IMAGE_HEIGHT]

    Returns:

    """
    string_image = base64_to_bytes(base64string)
    buffered2 = BytesIO(string_image)
    img2 = Image.open(buffered2)
    if image_size is not None:
        img2 = img2.resize(image_size)
    img2_array = np.asarray(img2)
    return img2_array


def image_to_base64(imagepath, image_size, image_format='PNG'):
    """reads image from a filepath or file object and converts it into base64

    Args:
        imagepath:
        image_size(list[int]): image size of format [IMAGE_WIDTH, IMAGE_HEIGHT]

    Returns:

    """
    img = Image.open(imagepath)
    img = img.resize(image_size, resample=PIL.Image.ANTIALIAS)
    buffered = BytesIO()
    img.save(buffered, format=image_format)
    imgstr = buffered.getvalue()
    base64_image = bytes_to_base64(imgstr)

    return base64_image


def urlimage_to_base64(url,image_size, timeout=10):
    """fetches image from a url and converts it to base64
    Args:
        timeout (int): time in seconds
        url(str):
        image_size(list[int]): image size of format [IMAGE_WIDTH, IMAGE_HEIGHT]

    Returns:
        str: base64 string

    """
    response = requests.get(url, timeout=timeout, headers=headers)
    img_bytesIO = BytesIO(response.content)
    img_base64 = image_to_base64(img_bytesIO, image_size)
    return img_base64


def post(url, data, headers=None, max_retry=3, wait=2, json=True, debug=False):
    retry = 1
    while retry <= max_retry:
        try:
            response = None
            if json == True:
                response = requests.post(url, headers=headers, json=data)
            else:
                response = requests.post(url, headers=headers, data=data)

            code = response.status_code
            response_text = response.text
            if code != 200:
                raise Exception(response_text)

            return response_text
        except Exception as e:
            msg = str(e)
            msg = msg if len(msg) < 200 else msg[:200]
            st = traceback.format_exc()
            print(msg)
            if debug == True:
                print(st)

        time.sleep(wait)
        retry += 1
    raise Exception("failed to complete request in the given retries")


def get(url, data=None, headers=None, max_retry=3, wait=2, debug=False):
    retry = 1
    while retry <= max_retry:
        try:
            response = None
            response = requests.get(url, params=data)
            code = response.status_code
            response_text = response.text
            if code != 200:
                raise Exception(response_text)

            return response_text
        except Exception as e:
            msg = str(e)
            msg = msg if len(msg) < 200 else msg[:200]
            st = traceback.format_exc()
            print(msg)
            if debug == True:
                print(st)

        time.sleep(wait)
        retry += 1
    raise Exception("failed to complete request in the given retries")

def generate_randomstring():
    digits = "".join([str(np.random.choice(list(string.digits),1)[0]) for i in range(8)] )
    chars = "".join( [str(np.random.choice(list(string.ascii_letters),1)[0]) for i in range(15)] )
    val = (digits + chars)
    return val


def api_extract_test(json_request):
    """extracts the test from api json request

    Args:
        json_request(dict):

    Returns:

    """

    if not isinstance(json_request, dict):
        raise ValueError("json body must be a dictionary")
    test = json_request.get("test", [])

    if len(test) == 0:
        raise ValueError("test cannot be empty")

    return test

def api_convert_base64_images(b64_images, image_size= [128,128,]):
    """converts a list of base64 images to json
    compliant list of images

    Args:
        image_size (list): list of format [H, W]. pass None to disable resizing
        data(list[str]): list of base64 images

    Returns:
        list: returns a list of images of dimention
            image_width, image_height, channels


    """

    try:
        images = [base64_to_imagearray(i, image_size) for i in b64_images]

    except:
        raise ValueError("base64 decode error")

    return images

def api_ok(result):
    """forms an ok response

    Args:
        result (object): json compliant result i.e serializable

    Returns:
        str: returns a json string


    """
    response = {'result': result, 'errors': None}

    response_json = jsonify(response)
    return response_json


def format_url(url):
    """format the url string into a valid url id possible

    Args:
        url (str): the url string
    """
    if url == "":
        return url

    if not url.startswith('http'):
        url = "//" + url
        u = urlparse(url)
        u = u._replace(scheme='http')
        url = u.geturl()

    return url

