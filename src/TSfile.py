import os
import requests
import re
from natsort import natsorted
from tqdm import tqdm
from threading import Thread


class TSfile:
    def __init__(self, url) -> None:
        self.url = url

    def downloadTS(self):
        with open('playlist.m3u8', 'r') as f:
            for line in tqdm(f):
                duration = re.findall(r"([0-9]{1,5}).ts", line)
                if duration:
                    r = requests.get(self.url + "{}.ts".format(duration[0]))
                    with open(os.path.join("./ts_files", "{}.{}".format(duration[0], "ts")), "wb") as fd:
                        fd.write(r.content)


    def mergeTS(self, path: str, outputName: str):
        tsDir = natsorted(os.listdir(path))
        
        with open(outputName, "wb+") as f:
            for i in tqdm(range(len(tsDir) - 1)):
                dir = os.path.join("./ts_files", tsDir[i])
                f.write(open(dir, "rb").read())
        print("Completed merging!")
