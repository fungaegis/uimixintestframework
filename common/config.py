import json

from common.constant import Path


def get_web_conf():
    file = Path.CONF_DIR + "/config_web.json"
    with open(file, "r") as conf:
        config = json.load(conf)
    return config


def get_app_conf():
    file = Path.CONF_DIR + "/config_app.json"
    with open(file, "r") as conf:
        config = json.load(conf)
    return config


def get_caps():
    path = Path.CONF_DIR + "/caps.json"
    with open(path, "r") as file:
        caps = json.load(file)
    return caps
