from pathlib import Path

import requests


def make_folder(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)


def download_image(url, filename, folder):
    make_folder(folder)
    filename = Path.cwd() / folder / filename

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)
