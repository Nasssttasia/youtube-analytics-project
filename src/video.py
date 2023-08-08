import os

import self as self
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.__info_to_print = self.get_info_video()
        self.video_title = self.__info_to_print['items'][0]['snippet']['title']
        self.view_count = self.__info_to_print['items'][0]['statistics']['viewCount']
        self.like_count = self.__info_to_print['items'][0]['statistics']['likeCount']
        self.comment_count = self.__info_to_print['items'][0]['statistics']['commentCount']

    def get_info_video(self):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        return video_response

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, pl_id):
        super().__init__(video_id)
        self.pl_id = pl_id

    def __str__(self):
        return self.video_title
