# Any2Stem
This Python package enables you to extract an instrumental from any public Youtube video (or from a playlist, file or from a folder) using Deezer's Spleeter AI.

# Quickstart
Import `Stem` from `Any2Stem.classes` and create a `Stem` object. Currently `Stem` provides 4 ways to extract instrumentals.

**Example code**
```python
import os
import sys
from Any2Stem.classes import Stem

# Gets the current execution path
execution_path = os.path.dirname(os.path.realpath(
        os.path.abspath(sys.argv[0])
        ))


def main():
    # Creates a stem object with path being the execution path
    stem = Stem(path=execution_path)

    # Extracts a video
    stem.extract_from_yt(
            "https://www.youtube.com/watch?v=2N--RorISzo",
            output_path=os.path.join(execution_path, "audio_output")
            )

    # Opens the last added folder
    stem.open_last_folder()


if __name__ == "__main__":
    main()

```


**Functions**

| Function                   | Description                                                                               |
|----------------------------|-------------------------------------------------------------------------------------------|
| `extract_file`             | Extracts one file                                                                         |
| `extract_from_folder`      | Extracts all files in a folder                                                            |
| `extract_from_yt_playlist` | Iterates through all videos in a given playlist and extracts them using `extract_from_yt` |
| `open_last`                | Opens last added song                                                                     |
| `open_last_folder`         | Opens last added song folder                                                              |


**Parameters**

kwargs will always be passed to `extract_file`.

| `__init__` parameters | Description                                                                   |
|-----------------------|-------------------------------------------------------------------------------|
| `path`                | Working path                                                                  |
| `stems_type`          | Will be passed to `Spleeter.separate.Separate`, default = `"spleeter:2stems"` |
| `bit_rate`            | Will be passed to `Spleeter.separate.Separate`, default = `320`               |
| `codec`               | Will be passed to `Spleeter.separate.Separate`, default = `"mp3"`             |

| `extract_file` parameters | Description                                          |
|---------------------------|------------------------------------------------------|
| `file_path`               | Path to file which should be extracted               |
| `output_path`             | Output path                                          |
| `print_progress`          | Wether the current progress should be printed or not |
| `automatic_cleanup`       | Wether the `tmp_path` should be cleared or not       |
|                           |                                                      |

| `extract_from_folder` parameters | Description                                                                   |
|----------------------------------|-------------------------------------------------------------------------------|
| `folder_path`                    | Path to folder which contains the files                                       |
| `output_path`                    | Output path                                                                   |
| `skip_same_names`                | If `True`, songs will be skipped, if the name already exists in `output_path` |
| `**kwargs`                       | Will be passed to `extract_file`                                              |

| `extract_from_yt` parameters | Description                                                                                       |
|------------------------------|---------------------------------------------------------------------------------------------------|
| `link`                       | Link to Youtube video                                                                             |
| `output_path`                | Output path                                                                                       |
| `tmp_path`                   | Temporary path where downloaded and extracted videos will be saved                                |
| `print_progress`             | Wether the current progress should be printed or not                                              |
| `skip_same_names`            | If `True`, songs will be skipped, if the name already exists in `output_path`                     |
| `fast_forward`               | If `True`, songs will be skipped, if the title (Youtube video title) already exists in `tmp_path` |
| `**kwargs`                   | Will be passed to `extract_file`                                                                  |

| `extract_from_yt_playlist` parameters | Description                                          |
|---------------------------------------|------------------------------------------------------|
| `playlist_link`                       | Link to Youtube playlist                             |
| `print_progress`                      | Wether the current progress should be printed or not |
| `**kwargs`                            | Will be passed to `extract_file`                     |

# License
You can do whatever you want but you have to give credits.

# Documentation
I'll add more to this documentation, but I haven't much time currently, if you want to help me, just contact me.
