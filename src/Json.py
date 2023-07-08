import yaml


class JsonManager:
    def __init__(self, yaml_path: str):
        """Json Manager

        Args:
            yaml_path (str): path of yaml
        """
        self.yaml_path = yaml_path
        self.config = None

        self.yamlLoader()

    def yamlLoader(self) -> dict:
        """Load yaml

        Returns:
            dict: .yaml file data
        """
        with open(self.yaml_path, "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
            return self.config

    @property
    def streamId(self) -> str:
        """
        Returns:
            str: stream-id
        """
        return str(self.config["streamId"])

    @property
    def ts_directory(self) -> str:
        """
        Returns:
            str: ts folder | e.g. ./ts_files
        """
        return self.config["files"]["ts-directory"]

    @property
    def ts_output_file(self) -> str:
        """
        Returns:
            str: output file | e.g. ./output.ts
        """
        return self.config["files"]["ts-output-file"]

    @property
    def mp4_output_file(self) -> str:
        """
        Returns:
            str: output mp4 | e.g. ./output.mp4
        """
        return self.config["files"]["mp4-output-file"]

    @property
    def playlist_file(self) -> str:
        """
        Returns:
            str: m3u8 file | e.g. ./playlist.m3u8
        """
        return self.config["files"]["playlist-file"]
