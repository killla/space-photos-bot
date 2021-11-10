import datetime
import os
from urllib.parse import urlparse, unquote

from environs import Env
import requests

from image_tools import download_image


def get_ext(url):
    image_path = urlparse(unquote(url)).path
    ext = os.path.splitext(image_path)[-1]
    return ext


def fetch_nasa_apod(nasa_api_token, count, folder):
    url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_token}&count={count}'
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()

    for image_number, image in enumerate(images):
        if 'url' in image:  # skip pages without url
            image_url = image['url']
            ext = get_ext(image_url)
            if ext:  # skip videos
                filename = f'nasa{image_number}{ext}'
                download_image(image_url, filename, folder)


def fetch_nasa_epic(nasa_api_token, folder):
    url = f'https://api.nasa.gov/EPIC/api/natural/images?api_key={nasa_api_token}'
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()
    for image_number, image in enumerate(images):
        date = datetime.datetime.fromisoformat(image['date'])
        name = image['image']
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{date.year}/{date:%m}/{date:%d}/png/{name}.png?api_key={nasa_api_token}'
        filename = f'{name}{image_number}.png'
        download_image(image_url, filename, folder)


if __name__ == '__main__':
    folder_apod = 'nasa_apod'
    folder_epic = 'nasa_epic'
    env = Env()
    env.read_env()
    nasa_api_token = env.str('NASA_API_TOKEN')
    count = env.int('NASA_IMAGE_COUNT', 10)

    fetch_nasa_epic(nasa_api_token, folder_epic)
    fetch_nasa_apod(nasa_api_token, count, folder_apod)
