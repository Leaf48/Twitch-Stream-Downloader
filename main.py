from src.Twitch import TwitchStream
from src.TSfile import TSFileManager


if __name__ == "__main__":
    videoId = TSFileManager.yamlLoader("config.yaml")

    twitch = TwitchStream(videoId=videoId, playlist_file="./playlist.m3u8")
    twitch_url = twitch.downloadM3U8List()

    tsm = TSFileManager(
        url=twitch_url,
        ts_dir="./ts_files",
        playlist_file="./playlist.m3u8",
        output_ts_file="./output.ts",
        output_mp4_file="./original.mp4",
    )

    tsm.downloadTS()
    tsm.mergeTS()
    tsm.createMP4(True)
    tsm.deleteCache()
