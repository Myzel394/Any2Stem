import os
import shutil
import youtube_dl
from spleeter.separator import Separator
from termcolor import colored

"""
@misc{spleeter2019,
  title={Spleeter: A Fast And State-of-the Art Music Source Separation Tool With Pre-trained Models},
  author={Romain Hennequin and Anis Khlif and Felix Voituret and Manuel Moussallam},
  howpublished={Late-Breaking/Demo ISMIR 2019},
  month={November},
  note={Deezer Research},
  year={2019}
}"""

important_color = "yellow"


class NoLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download_done_hook(d):
    if d["status"] == "finished":
        print("Video was downloaded. Converting...")


class Stem:
    def __init__(
            self,
            path: str,
            stems_type: str = "spleeter:2stems",
            bit_rate: int = 320,
            codec: str = "mp3"
            ):

        self.path = path
        self.stems_type = stems_type
        self.bit_rate = bit_rate
        self.codec = codec

        self._default_output = os.path.abspath(os.path.join(self.path, "output"))
        self._default_tmp = os.path.abspath(os.path.join(self.path, "tmp"))

        self.last_file = None
        self.last_folder = None

    @staticmethod
    def __default__open_last(value):
        if not value:
            raise FileNotFoundError("You haven't extracted a song yet!")

        os.startfile(value)

    def open_last(self):
        self.__default__open_last(self.last_file)

    def open_last_folder(self):
        self.__default__open_last(self.last_folder)

    def __default__get_path(self, value, default, allow_same_name=False):
        def get_path(value, default):
            if value is None:
                return default

            if not os.path.isabs(value):
                return os.path.abspath(os.path.join(self.path, value))

            return value

        path = get_path(value, default)

        if not allow_same_name:
            base_path = path
            counter = 1

            while os.path.exists(path):
                path = base_path + "_" + str(counter)
                counter += 1

        return path

    def __get_tmp_path(self, path):
        return self.__default__get_path(path, self._default_tmp, allow_same_name=True)

    def __get_output_path(self, path):
        return self.__default__get_path(path, self._default_output, allow_same_name=True)

    def reset_default_tmp(self):
        shutil.rmtree(self._default_tmp)
        os.mkdir(self._default_tmp)

    def _check_title_exists(self, path, title):
        path = os.path.abspath(os.path.join(path, title))

        if os.path.exists(path):
            if len([x for x in os.listdir(path) if x.endswith(".mp3")]) >= 2:
                return True

        return False

    def extract_file(
            self,
            file_path: str,
            output_path: str = None,
            print_progress: bool = True,
            automatic_cleanup: bool = False,
            ):
        output_path = self.__get_output_path(output_path)

        if print_progress:
            print(
                    "Extracting ",
                    colored('"' + file_path + '"', important_color),
                    " now...",
                    sep=""
                    )

        separator = Separator(self.stems_type)
        separator.separate_to_file(
                file_path,
                output_path,
                codec=self.codec
                )

        self.last_file = file_path
        self.last_folder = output_path

        if print_progress:
            print(
                    colored('"' + file_path + '"', important_color),
                    " was extracted using stems_type: ",
                    colored('"' + self.stems_type + '"'),
                    " You can find it in path:",
                    colored('"' + output_path + '"', important_color),
                    sep=""
                    )

        if automatic_cleanup:
            self.reset_default_tmp()

    def extract_from_folder(
            self,
            folder_path: str,
            output_path: str = None,
            skip_same_names: bool = True,
            **kwargs
            ):
        output_path = self.__default__get_path(output_path, os.path.abspath(os.path.join(folder_path, "extracted")))

        for file in os.listdir(folder_path):
            path = os.path.abspath(os.path.join(folder_path, file))
            if self._check_title_exists(folder_path, file) and skip_same_names:
                print(
                        "Skipping ",
                        colored('"' + path + '"', important_color),
                        " because it already exists.",
                        sep=""
                        )
            else:
                self.extract_file(
                        file_path=path,
                        output_path=output_path,
                        **kwargs
                        )

    def get_ydl_options(self, tmp_path: str, print_progress: bool = True):
        data = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.codec,
                'preferredquality': str(self.bit_rate),
                }],
            "outtmpl": os.path.join(tmp_path, "%(title)s.%(ext)s"),
            "logger": NoLogger(),
            "progress_hooks": [],
            "ignoreerrors": True,
            }

        if print_progress:
            data["progress_hooks"] = [download_done_hook]

        return data

    def extract_from_yt(
            self,
            link: str,
            output_path: str= None,
            tmp_path: str = None,
            print_progress: bool = True,
            skip_same_names: bool = True,
            fast_forward: bool = True,
            **kwargs
            ):
        tmp_path = self.__get_tmp_path(tmp_path)
        output_path = self.__get_output_path(output_path)

        # Options for video downloading
        ydl_opts = self.get_ydl_options(tmp_path, print_progress)

        if print_progress:
            print(
                    "Downloading ",
                    colored('"' + link + '"', important_color),
                    " now...",
                    sep=""
                    )

        # Downloads video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)

            title = info.get("title")
            title_format = title + ".mp3"

            if skip_same_names and self._check_title_exists(output_path, title):
                print(
                        "Skipping ",
                        colored('"' + title + '"', important_color),
                        " (That's the title) because it already exists.",
                        sep=""
                        )
                return

            path = os.path.abspath(os.path.join(tmp_path, title_format))

            if fast_forward and os.path.exists(path):
                    print(
                            "Found file ",
                            colored('"' + title_format + '"', important_color),
                            " in ",
                            colored('"' + tmp_path + '"', important_color),
                            ". Continue using this instead of re-downloading it. Change ",
                            colored('"fast_forward"', "green"),
                            " to 'False' to disable that.",
                            sep=""
                            )
                    return

            ydl.download([link])

        # Gets file from tmp
        file_path = os.path.abspath(os.path.join(tmp_path, title_format))

        self.extract_file(
                file_path=file_path,
                print_progress=print_progress,
                **kwargs
                )

    def extract_from_yt_playlist(
            self,
            playlist_link: str,
            output_path: str = None,
            print_progress: bool = True,
            **kwargs
            ):
        output_path = self.__get_output_path(output_path)

        # Options for video downloading
        ydl_opts = self.get_ydl_options(output_path, print_progress)
        ydl_opts["noplaylist"] = False

        # Downloads video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_link, download=False)

            if "entries" in result:
                videos = result["entries"]

                for video in videos:
                    url = video["webpage_url"]
                    self.extract_from_yt(
                            link=url,
                            output_path=output_path,
                            print_progress=print_progress,
                            **kwargs
                            )



