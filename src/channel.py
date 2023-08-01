import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self._init_from_api()

    @classmethod
    def get_service(cls, self=None):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        service = json.dumps(channel, indent=2, ensure_ascii=False)
        return service

    def _init_from_api(self):
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute())

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails'][0]['default']['url']
        self.subscribers = channel['items'][0]['statistics'][0]['subscriberCount']
        self.videos = channel['items'][0]['statistics'][0]['videoCount']
        self.views = channel['items'][0]['statistics'][0]['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        return print(self.get_service())

    def to_json(self):
        with open ('moscowpython.json', 'w') as file:
            json.dump(self.get_service(), file)