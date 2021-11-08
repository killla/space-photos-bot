import requests

from image_tools import download_image


def fetch_launch(launch_id, folder):
    url = f'https://api.spacexdata.com/v4/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()['links']['flickr']['original']

    for image_number, image_link in enumerate(images):
        filename = f'spacex{image_number}.jpg'
        download_image(image_link, filename, folder)


def find_last_launch_with_images():
    url = 'https://api.spacexdata.com/v4/launches/past'
    response = requests.get(url)
    response.raise_for_status()
    launches = response.json()
    for launch in launches[::-1]:
        image = launch['links']['flickr']['original']
        if image:
            return launch['id']


def fetch_spacex_last_launch(folder):
    launch_id = find_last_launch_with_images()
    fetch_launch(launch_id, folder)


if __name__ == '__main__':
    folder = 'spacex'
    fetch_spacex_last_launch(folder)
