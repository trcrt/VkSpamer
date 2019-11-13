import vk_api
import json
import logging
import schedule
import time
import random

import schedule_utils

CONFIG_FILENAME = './config.json'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',)


class Messenger(object):

    def __init__(self, token):
        super(Messenger, self).__init__()
        self.token = token
        self.reauth()

    def reauth(self):        
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
        self.upload = vk_api.VkUpload(self.vk_session)

    def _send(self, target_id, message):
        random_id = random.randint(-2000000, 2000000)
        self.vk.messages.send(peer_id=target_id, random_id=random_id, message=message)
        logging.info('Сообщение отправлено.')

    def send(self, target_id, message):
        logging.info('Отправляем сообщение: "{}", пользователю {}...'.format(message, target_id))
        try:
            self._send(target_id, message)
        except Exception as e:
            logging.exception('Ошибка при отправке сообщения. Пытаемся переавторизоваться и повторить...')
            self.reauth()
            self._send(target_id, message)


class Spammer(object):

    def __init__(self, config):
        super(Spammer, self).__init__()

        messages_filename = config['messages_file']
        with open(messages_filename) as file:
            self.messages = file.read().strip().splitlines()
        self.target_id = config['target_id']
        self.messenger = Messenger(config['access_token'])
        self.schedule = Spammer.get_schedule_from_config(config)
        self.skip_first_message = config.get('skip_first_message', False)
    
    @staticmethod
    def get_schedule_from_config(config):
        delay_min, delay_max = config['message_delay_range']
        return schedule.every(delay_min).to(delay_max).seconds

    def run(self):
        @schedule_utils.catch_exceptions
        def messaging_job():
            message = random.choice(self.messages)
            self.messenger.send(self.target_id, message)
        
        logging.info('Запускаем очередь отправки сообщений...')
        self.schedule.do(messaging_job)

        if not self.skip_first_message:
            logging.info('Отправляем первое сообщение...')
            messaging_job()
        else:
            logging.info('Ожидаем наступления времени, указанного в расписании...')

        while True:
            schedule.run_pending()
            time.sleep(1)


def main():
    with open(CONFIG_FILENAME) as file:
        config = json.load(file)
    spammer = Spammer(config)
    spammer.run()


if __name__ == '__main__':
    main()