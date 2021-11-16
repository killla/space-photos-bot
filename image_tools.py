from pathlib import Path

import requests


def download_image(url, filename, folder, payload=None):
    Path(folder).mkdir(parents=True, exist_ok=True)
    file_path = Path.cwd() / folder / filename

    response = requests.get(url, params=payload)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(response.content)
