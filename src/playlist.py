import os

import isodate
from googleapiclient.discovery import build

class PlayList:

    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.__info_to_print = self.get_info_pl()
        # self.__pl_title = self.__info_to_print['items'][0]['snippet']['title'] как прописать путь?
        # self.__pl_url = self.__info_to_print['items'][0]['statistics']['viewCount']

    @property
    def title(self):
        return self.__pl_title

    @property
    def url(self):
        return self.__pl_url

    def get_info_pl(self):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        pl_response = youtube.playlists().list(channelId=self.pl_id,
                                     part='contentDetails,snippet',
                                     maxResults=50,
                                     ).execute()
        return pl_response

    def total_duration(self):
        """возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        (обращение как к свойству, использовать `@property`)"""
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=self.pl_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            return duration

    @property
    def total_duration(self):
        return self.total_duration()

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        pass