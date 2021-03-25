import os


class Path:
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    SCREENSHOT_PATH = os.path.join(BASE_PATH, "screenshot")

    LOG_PATH = os.path.join(BASE_PATH, "logs")

    CONF_DIR = os.path.join(BASE_PATH, "conf")

    DRIVER_DIR = os.path.join(BASE_PATH, "WebDriver")


class Resolution:
    SIZE_4K = "--window-size=4096,2160"
    SIZE_1080P = "--window-size=1920,1080"
