import os
import requests
import re
from natsort import natsorted
from tqdm import tqdm
import yaml
import subprocess
import os


class TSFileManager:
    def __init__(
        self,
        url,
        ts_dir: str,
        playlist_file: str,
        output_ts_file: str,
        output_mp4_file: str,
    ) -> None:
        # BASEURL
        # https://...
        self.url = url

        # ts saved directory
        # ./ts_files
        self.ts_dir = ts_dir

        # playlist.m3u8
        self.playlist_file = playlist_file

        # output file
        # ./output.ts
        self.output_ts_file = output_ts_file

        # output file
        # ./output.mp4
        self.output_mp4_file = output_mp4_file

    # Download all .ts file
    def downloadTS(self):
        with open(self.playlist_file, "r") as f:
            for line in tqdm(f):
                duration = re.findall(r"([0-9]{1,5}).ts", line)
                if duration:
                    while True:
                        try:
                            r = requests.get(self.url + "{}.ts".format(duration[0]))
                            with open(
                                os.path.join(
                                    self.ts_dir, "{}.{}".format(duration[0], "ts")
                                ),
                                "wb",
                            ) as fd:
                                fd.write(r.content)
                            break
                        except:
                            pass
        print("Download Completed!")

    # Merge all .ts file into one file
    def mergeTS(self):
        tsDir = natsorted(os.listdir(self.ts_dir))

        with open(self.output_ts_file, "wb+") as f:
            for i in tqdm(range(len(tsDir) - 1)):
                dir = os.path.join(self.ts_dir, tsDir[i])
                f.write(open(dir, "rb").read())

        print("Merging Completed!")

    # Load yaml file
    def yamlLoader(self, yaml_path: str = "config.yaml") -> str:
        with open(yaml_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return str(config["streamId"])

    # Create mp4 from .ts
    def createMP4(self, verbose: bool = False):
        command = "ffmpeg -i {} -c:v copy -c:a copy {}".format(
            self.output_ts_file, self.output_mp4_file
        )
        res = subprocess.run(command, shell=True)

        if verbose:
            print(res)

    # Remove all .ts file
    def deleteCache(self):
        for filename in os.listdir(self.ts_dir):
            if filename.endswith(".ts"):
                os.remove("{}/{}".format(self.ts_dir, filename))

        os.remove(self.output_ts_file)
        os.remove(self.playlist_file)

        print("Removed all cache")
