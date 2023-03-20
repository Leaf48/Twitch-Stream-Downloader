from src.Twitch import Twitch
from src.TSfile import TSfile

if __name__ == "__main__":
    t = Twitch().downloadM3U8List("")

    ts = TSfile(t)
    ts.downloadTS()
    ts.mergeTS("./ts_files", "output.ts")
