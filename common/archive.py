import os
import re
import shutil
from common.constant import Path
from common.logger import logger


def archive_file(filepath=Path.SCREENSHOT_PATH, pattern=r"[\w\]\[]*\.png") -> None:  # TODO: 递归实现
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    else:
        dirs_list = os.listdir(filepath)
        for dir_name in dirs_list:
            path = os.path.join(filepath, dir_name)
            if not os.path.isdir(path):
                continue
            dirs = ';'.join(os.listdir(path))
            mv_dirs = re.findall(pattern, dirs)
            if mv_dirs:
                history = os.path.join(filepath, "history", dir_name)
                if not os.path.exists(history):
                    os.makedirs(history)
                times = 1
                while True:
                    existing = os.path.join(history, str(times))
                    if not os.path.exists(existing):
                        os.makedirs(existing)
                        break
                    times += 1
                for i in mv_dirs:
                    shutil.move(os.path.join(path, i), existing)
                else:
                    try:
                        os.removedirs(path)
                    except OSError as e:
                        logger.warning(f"Delete directory path:{path} error! Track:{e}")
