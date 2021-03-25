import pytest
import platform

from selenium import webdriver
from common.constant import Path, Resolution
from common.context import Context


def local_driver(options):
    if platform.system() == "Linux":
        driver = webdriver.Chrome(executable_path=Path.DRIVER_DIR + "/chromedriver", options=options)
    else:
        driver = webdriver.Chrome(executable_path=Path.DRIVER_DIR + "/chromedriver.exe", options=options)


@pytest.fixture(scope="class")
def driver():
    command_executor = getattr(Context, "SERVICE")
    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument(Resolution.SIZE_1080P)
    # local_driver(options)
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    driver = webdriver.Remote(command_executor=command_executor, desired_capabilities=caps, options=options)
    driver.implicitly_wait(30)
    env = getattr(Context, "ENV")
    url = env["service"]["web"]
    driver.get(url)
    yield driver
    driver.close()
    driver.quit()
