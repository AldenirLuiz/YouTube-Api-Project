from googleapiclient.discovery import build


class MyYoutube:
    def __init__(self, userApi_Key:str, vId:str) -> None:
        self.user_key:str = userApi_Key 
        self.youtube:build = build("youtube", "v3", developerKey=self.user_key, )
        self.id:str = vId
        self.container_videos = list()

    def showVideoInfo(self):
        try:
            my_request = self.youtube.playlistItems().list(
                part="snippet", playlistId=self.id, maxResults=100
            ).execute()
            return my_request
        except:
            self.youtube.search().list(
                q=self.id, part="id, snippet", playlistId=self.id, maxResults=100
            ).execute()
        return 
