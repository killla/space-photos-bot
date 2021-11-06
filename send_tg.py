from fetch_spacex import fetch_spacex_last_launch
from fetch_nasa import fetch_nasa_epic

import telegram
from environs import Env

import time
import os

env = Env()
env.read_env()
TG_BOT_TOKEN = env.str('TG_BOT_TOKEN')
TG_CHANNEL = env.str('TG_CHANNEL')
PERIOD = env.int('TG_PERIOD', 86400)
bot = telegram.Bot(token=TG_BOT_TOKEN)


def send_image(filename):
    bot = telegram.Bot(token=TG_BOT_TOKEN)
    bot.send_photo(chat_id=TG_CHANNEL, photo=open(filename, 'rb'))


def images(dirname):
    for image in os.listdir(dirname):
        yield os.path.join(dirname, image)


if __name__ == '__main__':
    while True:
        fetch_spacex_last_launch()
        fetch_nasa_epic()
        for image in images('spacex'):
            send_image(image)
            os.remove(image)
        for image in images('nasa'):
            send_image(image)
            os.remove(image)
        time.sleep(PERIOD)
