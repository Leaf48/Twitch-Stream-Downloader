from src.Twitch import Twitch
from src.TSfile import TSfile
import yaml
import subprocess
import os

def yamlLoader():
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config["streamId"]
        

if __name__ == "__main__":
    config = yamlLoader()
    
    t = Twitch().downloadM3U8List("{}".format(config))

    ts = TSfile(t)
    ts.downloadTS()
    ts.mergeTS("./ts_files", "output.ts")

    # Start convert output.ts to output.mp4
    command = "ffmpeg -i output.ts -c:v copy -c:a copy output.mp4"
    res = subprocess.run(command, shell=True)
    print(res)
    
    # remove all .ts file
    for filename in os.listdir("./ts_files"):
        if filename.endswith(".ts"):
            os.remove("./ts_files/{}".format(filename))
    os.remove("./output.ts")
    os.remove("./playlist.m3u8")

    
