import pytest
import subprocess
import platform
from selenium.webdriver.common.utils import free_port
from appium.webdriver.appium_service import AppiumService
from appium import webdriver

from common.config import get_caps
from common.context import Context


class Command:

    @classmethod
    def __cmd_run(cls, command):
        try:
            out, err = \
                subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            out = str(out, encoding="utf8").strip()
            err = str(err, encoding="uft8").strip()
            if err:
                raise Exception("run command error {}".format(err))
        except Exception as e:
            raise e
        else:
            return out

    def devices_and_version(self):
        devices_uuid = self.__get_devices()
        versions = self.__get_version(devices_uuid)
        res = list(zip(devices_uuid, versions))
        return res

    def __get_devices(self):
        command = "adb devices"
        res = self.__cmd_run(command)

        if platform.system() == "Windows":
            res = res.split("\r\n")
        elif platform.system() == "Linux":
            res = res.split("\n")
        else:
            raise TypeError("Platform Error")

        res.remove("List of devices attached")

        devices = []
        for item in res:
            if "device" in item:
                s = item.split("\t")
                if s[1] == "device":
                    devices.append(s[0])
        return devices

    def __get_version(self, uuids):
        command = "adb -s {} shell getprop ro.build.version.release"
        versions = []
        for uuid in uuids:
            version = self.__cmd_run(command.format(uuid))
            versions.append(version)
        return versions


def base_args(*port, **kwargs):
    if not port:  # 寻找空闲端口
        port = free_port()
    caps = get_caps()
    caps.update(getattr(Context, "ENV")["caps"])
    devices = Command().devices_and_version()
    n = 0
    if kwargs:
        for key, value in kwargs.items():
            caps[key] = value
    for res in devices:
        caps["deviceName"] = res[0]
        caps["platformVersion"] = res[1]
        service = AppiumService()
        service.start(args=["-a", "127.0.0.1", "-p", port[n], "--session-override"], timeout_ms=2000)
        driver = webdriver.Remote(command_executor='http://127.0.0.1:{}/wd/hub'.format(port[n]),
                                  desired_capabilities=caps)
        yield driver
        service.stop()


@pytest.fixture(scope="class")
def start(**kwargs):
    port = str(free_port())
    devices = Command().devices_and_version()[0]
    caps = get_caps()["devices"]["samsung-10"]
    caps.update(getattr(Context, "CAPS"))
    if kwargs:
        for key, value in kwargs.items():
            caps[key] = value
    caps["deviceName"] = devices[0]
    caps["platformVersion"] = devices[1]
    service = AppiumService()
    service.start(args=["-a", "127.0.0.1", "-p", port, "--session-override"], timeout_ms=2000)
    driver = webdriver.Remote(command_executor=f'http://127.0.0.1:{port}/wd/hub',
                              desired_capabilities=caps)
    yield driver
    driver.close()
    driver.quit()
    service.stop()


if __name__ == '__main__':
    cmd = Command()
    print(cmd.devices_and_version())  # [('172.16.16.67:5555', '10')]
