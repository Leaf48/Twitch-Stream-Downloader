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
        """TS file

        Args:
            url (str): base-url
            ts_dir (str): directory that all .ts file are saved to
            playlist_file (str): playlist.m3u8
            output_ts_file (str): output .ts that all .ts were merged
            output_mp4_file (str): output .mp4
        """
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

    def downloadTS(self):
        """Download all .ts file"""
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

    def mergeTS(self):
        """Merge all .ts file into one file"""
        tsDir = natsorted(os.listdir(self.ts_dir))

        with open(self.output_ts_file, "wb+") as f:
            for i in tqdm(range(len(tsDir) - 1)):
                dir = os.path.join(self.ts_dir, tsDir[i])
                f.write(open(dir, "rb").read())

        print("Merging Completed!")

    def yamlLoader(self, yaml_path: str = "config.yaml") -> str:
        """Load yaml file and get video-id

        Args:
            yaml_path (str, optional): filename to be saved. Defaults to "config.yaml".

        Returns:
            str: video-id
        """
        with open(yaml_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return str(config["streamId"])

    def createMP4(self, verbose: bool = False):
        """Create mp4 from .ts

        Args:
            verbose (bool, optional): Is it shown info?. Defaults to False.
        """
        command = "ffmpeg -i {} -c:v copy -c:a copy {}".format(
            self.output_ts_file, self.output_mp4_file
        )
        res = subprocess.run(command, shell=True)

        if verbose:
            print(res)

    def deleteCache(self):
        """Remove all .ts file"""
        for filename in os.listdir(self.ts_dir):
            if filename.endswith(".ts"):
                os.remove("{}/{}".format(self.ts_dir, filename))

        os.remove(self.output_ts_file)
        os.remove(self.playlist_file)

        print("Removed all cache")
