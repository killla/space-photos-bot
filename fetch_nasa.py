import requests
from environs import Env

import os
import datetime
from pathlib import Path
from urllib.parse import urlparse

IMAGE_FOLDER = 'nasa'
env = Env()
env.read_env()
NASA_API_TOKEN = env.str('NASA_API_TOKEN')
COUNT = env.int('NASA_IMAGE_COUNT', 10)


def get_image(url, filename):
    Path(IMAGE_FOLDER).mkdir(parents=True, exist_ok=True)
    filename = Path.cwd() / IMAGE_FOLDER / filename

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_ext(url):
    image_path = urlparse(url).path
    image_filename = os.path.split(image_path)[-1]
    ext = os.path.splitext(image_filename)[-1]
    return(ext)


def fetch_nasa_apod():
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_TOKEN}&count={COUNT}'
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()

    for image_number, image in enumerate(images):
        if 'url' in image:  # skip pages without url
            image_url = image['url']
            ext = get_ext(image_url)
            if ext:  # skip videos
                filename = f'nasa{image_number}{ext}'
                get_image(image_url, filename)


def fetch_nasa_epic():
    url = f'https://api.nasa.gov/EPIC/api/natural/images?api_key={NASA_API_TOKEN}'
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()
    for image_number, image in enumerate(images):
        date = datetime.datetime.fromisoformat(image['date'])
        name = image['image']
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{date.year}/{date:%m}/{date:%d}/png/{name}.png?api_key={NASA_API_TOKEN}'
        filename = f'{name}{image_number}.png'
        get_image(image_url, filename)


if __name__ == '__main__':
    fetch_nasa_epic()
