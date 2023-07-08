import m3u8
import requests
import json


class TwitchStream:
    def __init__(self, videoId: str, playlist_file: str) -> None:
        """Twitch Stream Downloader

        Args:
            videoId (str): target video-id
            playlist_file (str): the path name to be saved | e.g. playlist.m3u8
        """
        self.clientId = "kimne78kx3ncx6brgo4mv6wki5h1ko"
        self.videoId = videoId
        # playlist.m3u8
        self.playlist_file = playlist_file

    def getToken(self) -> dict:
        """Get token of video

        Returns:
            dict: tokens
        """
        HEADERS = {"Client-id": self.clientId}

        PAYLOAD = json.dumps(
            [
                {
                    "operationName": "PlaybackAccessToken",
                    "extensions": {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712",
                        }
                    },
                    "variables": {
                        "isLive": True,
                        "login": "",
                        "isVod": True,
                        "vodID": self.videoId,
                        "playerType": "embed",
                    },
                }
            ]
        )

        RESPONSE = requests.post(
            "https://gql.twitch.tv/gql", headers=HEADERS, data=PAYLOAD
        )

        return RESPONSE.json()[0]["data"]["videoPlaybackAccessToken"]

    def downloadM3U8List(self) -> str:
        """Download m3u8 list

        Returns:
            str: base-url
        """
        VALUE = self.getToken()
        URL = "https://usher.ttvnw.net/vod/{}.m3u8?client_id={}&token={}&sig={}&allow_source=true&allow_audio_only=true".format(
            self.videoId, self.clientId, VALUE["value"], VALUE["signature"]
        )
        RESPONSE = requests.get(URL)

        splitFile = RESPONSE.text.split("\n")
        BASE_URL = ""
        for i in splitFile:
            if i.startswith("http"):
                BASE_URL = i
                break

        playlist = m3u8.load(BASE_URL)
        playlist.dump(self.playlist_file)

        fileName = BASE_URL[BASE_URL.rfind("/") + 1 :]
        BASE_URL = BASE_URL.replace(fileName, "")

        return BASE_URL
