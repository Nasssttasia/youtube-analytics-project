import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        youtube_channels_list = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics')
        self.__info_to_print = youtube_channels_list.execute()
        self.title = self.__info_to_print['items'][0]['snippet']['title']
        self.description = self.__info_to_print['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/{self.__info_to_print['items'][0]['snippet']['customUrl']}"
        self.subscribers = int(self.__info_to_print['items'][0]['statistics']['subscriberCount'])
        self.video_count = self.__info_to_print['items'][0]['statistics']['videoCount']
        self.view_count = self.__info_to_print['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__info_to_print, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        channel = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscribers': self.subscribers,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(filename, 'w', encoding="UTF-8") as file:
            json.dump(channel, file, ensure_ascii=False)

"""
    def __str__(self):
        return f"{self.title} {self.url}"

    def __add__(self, other):
        return self.subscribers + self.subscribers

    def __sub__(self, other):
        pass

    def __lt__(self, other):
        pass
"""
