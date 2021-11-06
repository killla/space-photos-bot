import requests

from pathlib import Path

IMAGE_FOLDER = 'spacex'


def get_image(url, filename):
    Path(IMAGE_FOLDER).mkdir(parents=True, exist_ok=True)
    filename = Path.cwd() / IMAGE_FOLDER / filename

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def fetch_launch(launch_id):
    url = f'https://api.spacexdata.com/v4/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()['links']['flickr']['original']

    for image_number, image_link in enumerate(images):
        filename = f'spacex{image_number}.jpg'
        get_image(image_link, filename)


def find_last_launch_with_images():
    url = 'https://api.spacexdata.com/v4/launches/past'
    response = requests.get(url)
    response.raise_for_status()
    launches = response.json()
    for launch in launches[::-1]:
        image = launch['links']['flickr']['original']
        if image:
            return launch['id']


def fetch_spacex_last_launch():
    launch_id = find_last_launch_with_images()
    fetch_launch(launch_id)


if __name__ == '__main__':
    fetch_spacex_last_launch()
