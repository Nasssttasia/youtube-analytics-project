import os
from datetime import datetime, timedelta

import isodate
from googleapiclient.discovery import build

class PlayList:

    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.__info_to_print = self.get_info_pl()
        self.__pl_title = self.__info_to_print['items'][0]['snippet']['title']
        self.__pl_url = f"https://www.youtube.com/playlist?list={self.__info_to_print['items'][0]['id']}"

    @property
    def title(self):
        return self.__pl_title

    @property
    def url(self):
        return self.__pl_url

    def get_info_pl(self):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        pl_response = youtube.playlists().list(id=self.pl_id, part='snippet').execute()
        return pl_response

    def get_info_video(self):
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
        return video_response

    @property
    def total_duration(self):
        """возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        (обращение как к свойству, использовать `@property`)"""
        video_response = self.get_info_video()
        duration = isodate.parse_duration("PT0S")
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)

        return duration


    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        return f"https://youtu.be/{self.get_info_video()['items'][3]['id']}"
