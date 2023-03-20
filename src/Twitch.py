import m3u8
import requests
import json

class Twitch:
    def __init__(self) -> None:
        self.CLIENT_ID = 'kimne78kx3ncx6brgo4mv6wki5h1ko'

    def getToken(self, videoId: str) -> dict:
        HEADERS = {
            "Client-id": self.CLIENT_ID
        }

        PAYLOAD = json.dumps([{
            "operationName": "PlaybackAccessToken",
            "extensions": {
                "persistedQuery": {
                "version": 1,
                "sha256Hash": "0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712"
                }
            },
            "variables": {
                "isLive": True,
                "login": '',
                "isVod": True,
                "vodID": videoId,
                "playerType": "embed"
            }
        }])

        RESPONSE = requests.post(
            "https://gql.twitch.tv/gql",
            headers=HEADERS,
            data=PAYLOAD
        )
        # print(RESPONSE.json())

        return RESPONSE.json()[0]["data"]["videoPlaybackAccessToken"]


    def downloadM3U8List(self, videoId: str) -> str:
        VALUE = self.getToken(videoId=videoId)
        URL = "https://usher.ttvnw.net/vod/{}.m3u8?client_id={}&token={}&sig={}&allow_source=true&allow_audio_only=true".format(
            videoId,
            self.CLIENT_ID,
            VALUE["value"],
            VALUE["signature"]
        )
        RESPONSE = requests.get(URL)
        
        splitFile = RESPONSE.text.split("\n")
        BASE_URL = ""
        for i in splitFile:
            if i.startswith("http"):
                BASE_URL = i
                break

        playlist = m3u8.load(BASE_URL)
        playlist.dump("playlist.m3u8")

        fileName = BASE_URL[BASE_URL.rfind("/") + 1:]
        BASE_URL = BASE_URL.replace(fileName, "")

        return BASE_URL