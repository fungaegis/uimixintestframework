# global function
import os
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from common.config import get_web_conf, get_app_conf, get_caps
from common.context import Context
from common.logger import logger


def pytest_addoption(parser):
    parser.addoption("-E", "--env", dest="env", action="store", default="test",
                     help="choice run environmental")  # 环境
    parser.addoption("-P", "--product", dest="product", action="store", default="B",
                     help="choice run product")  # 产品线
    parser.addoption("-S", "--service", dest="services", action="store", default="DEBUG",
                     help="choice run position")  # 远端服务
    parser.addoption("-M", "--mode", dest="mode", action="store", default="WEB", choices=["WEB", "APP"],
                     help="choice run mode")  # 运行模式
    parser.addoption("-A", "--app", dest="app", action="store", default="", help="APK Path")
    parser.addoption("--device", action="store", default="", help="Select the specified device")


@pytest.mark.tryfirst
def pytest_configure(config):
    mode = config.getoption("mode")
    env = config.getoption("env")
    product = config.getoption("product")
    service = config.getoption("services")
    if mode == "WEB":
        conf = get_web_conf()
    else:
        conf = get_app_conf()
        caps = conf[product]["caps"]
        app = config.getoption("app")
        if app:
            if not os.path.isfile(app):
                app = os.path.join(os.getcwd(), app)
            caps.update(app)
        device = config.getoption("device")
        if device:
            device = get_caps()["devices"][device]
            caps.update(device)
        setattr(Context, "CAPS", caps)

    env = conf[product]["env"][env]
    setattr(Context, "ENV", env)

    service = conf[product]["services"][service]
    setattr(Context, "SERVICE", service)

    prod = conf[product]["product"]
    setattr(Context, "PRODUCT", prod)

    logger.init()


def pytest_collection_modifyitems(config, items):
    mode = config.getoption("mode")
    product = getattr(Context, "PRODUCT")
    selected = []
    deselected = []
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        if mode == "APP" and fr"test_app/test_{product}" in item._nodeid:
            selected.append(item)
        elif mode == "WEB" and fr"test_web/test_{product}" in item._nodeid:
            selected.append(item)
        else:
            deselected.append(item)
    if deselected and mode in ("WEB", "APP"):
        config.hook.pytest_deselected(items=deselected)
        items[:] = selected


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call" and "test_web" in item.nodeid:
        for value in item.funcargs.values():
            if isinstance(value, WebDriver):
                if result.failed:
                    value.add_cookie({"name": "zaleniumTestPassed", "value": "false"})
                else:
                    value.add_cookie({"name": "zaleniumTestPassed", "value": "true"})
                break


def pytest_runtest_call(item):
    if "test_web" in item.nodeid:
        for value in item.funcargs.values():
            if isinstance(value, WebDriver):
                value.add_cookie({"name": "zaleniumMessage", "value": f"{item.name}"})
