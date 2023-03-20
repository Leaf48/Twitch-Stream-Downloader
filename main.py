from src.Twitch import Twitch
from src.TSfile import TSfile

if __name__ == "__main__":
    t = Twitch().downloadM3U8List("1769579662")

    ts = TSfile(t)
    ts.downloadTS()
    ts.mergeTS("./ts_files", "output.ts")
