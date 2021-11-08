from fetch_spacex import fetch_spacex_last_launch
from fetch_nasa import fetch_nasa_epic, fetch_nasa_apod

import telegram
from environs import Env

import time
import os


def send_image(filename, bot, tg_channel):
    with open(filename, 'rb') as image_file:
        bot.send_photo(chat_id=tg_channel, photo=image_file)


def get_image(folder):
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[-1] in ('.jpg', '.png'):
                yield os.path.join(dirpath, filename)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_bot_token = env.str('TG_BOT_TOKEN')
    tg_channel = env.str('TG_CHANNEL')
    period = env.int('TG_PERIOD', 86400)
    nasa_api_token = env.str('NASA_API_TOKEN', 'DEMO_KEY')
    count = env.int('NASA_IMAGE_COUNT', 10)
    bot = telegram.Bot(token=tg_bot_token)

    while True:
        for image in get_image('.'):
            send_image(image, bot, tg_channel)
            time.sleep(period)
            os.remove(image)  # избегаем повторной отправки одной и той же картинки
        fetch_spacex_last_launch('spacex')
        fetch_nasa_epic(nasa_api_token, 'nasa_epic')
        fetch_nasa_apod(nasa_api_token, count, 'nasa_apod')
