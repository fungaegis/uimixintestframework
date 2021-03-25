import pytest
from appium import webdriver

from common.command import start
from common.context import Context


@pytest.fixture(scope="class")
def driver():
    caps = getattr(Context, "CAPS")
    service = getattr(Context, "SERVICE")
    driver = webdriver.Remote(command_executor=service, desired_capabilities=caps)
    driver.implicitly_wait(120)
    driver.unlock()
    yield driver
    driver.quit()

