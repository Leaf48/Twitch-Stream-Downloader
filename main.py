from src.Twitch import TwitchStream
from src.TSfile import TSFileManager
from src.Json import JsonManager


if __name__ == "__main__":
    jsm = JsonManager("./config.yaml")

    twitch = TwitchStream(videoId=jsm.streamId, playlist_file=jsm.playlist_file)
    twitch_url = twitch.downloadM3U8List()

    tsm = TSFileManager(
        url=twitch_url,
        ts_dir=jsm.ts_directory,
        playlist_file=jsm.playlist_file,
        output_ts_file=jsm.ts_output_file,
        output_mp4_file=jsm.mp4_output_file,
    )

    tsm.downloadTS()
    tsm.mergeTS()
    tsm.createMP4(True)
    tsm.deleteCache()
