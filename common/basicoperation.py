import os
import time
import datetime
import pyautogui
import uuid

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from appium.webdriver.webdriver import WebDriver as AppDriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction
from appium.common.exceptions import NoSuchContextException

from common.constant import Path
from common.logger import logger


# class Driver(WebDriver, AppDriver):
#     pass


class BasicOperation:
    """
    Main save basic operation
    """

    def __init__(self, driver: AppDriver):
        self.driver = driver

    def capture_screen_shot(self, page_name):
        """Capture and save screen shot
        Scope: Mobile, Web
        :param page_name: screen shot photo name
        :return: None
        """
        img_path = os.path.join(Path.SCREENSHOT_PATH, time.strftime("%Y-%m-%d"))
        if not os.path.exists(img_path):
            os.makedirs(img_path)

        img_path = os.path.join(img_path, page_name.replace(" ", "_") + "_" + str(uuid.uuid4()).replace("-", "")[:8] + ".png")
        res = self.driver.save_screenshot(img_path)
        if not res:
            logger.error(f"Page: {page_name} Action: [capture_screen_shot] \n"
                         f"Msg:screen shot failed")
        else:
            logger.info(f"Page: {page_name} Action: [capture_screen_shot] \n"
                        f"Msg:screen shot successful path: {img_path}")
            return img_path

    def wait_ele_visible(self, page_name, loc, model="single", timeout=30, polling=0.5):
        """Wait element visible

        :param loc: locators(by, loc)
        :param page_name: page and object name
        :param model: wait type, default: single
        :param timeout: timeout(s) default=30s
        :param polling: polling(s) default=0,5s
        :return: None
        """
        start_time = datetime.datetime.now()
        try:
            if model == "all":  # full view element visible
                ele = WebDriverWait(self.driver, timeout, polling).until(ec.visibility_of_all_elements_located(loc))
            elif model == "single":  # specify element visible
                ele = WebDriverWait(self.driver, timeout, polling).until(ec.visibility_of_element_located(loc))
            elif model == "any":  # any visible
                ele = WebDriverWait(self.driver, timeout, polling).until(ec.visibility_of_any_elements_located(loc))
            else:
                raise TypeError(f"Wait element visible model: {model} is error")
        except exceptions.TimeoutException as e:
            logger.error(f"Page: {page_name} Action: [wait_ele_visible] Element：{loc} \n"
                         f"Msg:not visible failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        except TypeError as e:
            logger.error(f"Page: {page_name} Action: [wait_ele_visible] Element：{loc} \n"
                         f"Msg:Wait element visible model {model} is error")
            raise e
        else:
            end_time = datetime.datetime.now()
            logger.info(f"Page: {page_name} Action: [wait_ele_visible] Element: {loc} \n"
                        f"Msg:visible successful，waiting time:{end_time - start_time}")
            return ele

    def wait_ele_presence(self, page_name, loc, model="single", timeout=30, polling=0.5):
        """Wait element presence

        :param page_name: page and object name
        :param loc: locators(by, loc)
        :param model: wait type, default: single
        :param timeout: timeout(s) default=30s
        :param polling: polling(s) default=0,5s
        :return:
        """
        start_time = datetime.datetime.now()
        try:
            if model == "all":
                ele = WebDriverWait(self.driver, timeout, polling).until(ec.presence_of_all_elements_located(loc))
            elif model == "single":
                ele = WebDriverWait(self.driver, timeout, polling).until(ec.presence_of_element_located(loc))
            else:
                raise TypeError(f"Page: {page_name} Wait element presence model: {model} is error")
        except exceptions.TimeoutException as e:
            logger.error(f"Page: {page_name} Action: [wait_ele_presence] Element：{loc}\n"
                         f"Msg:not presence failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        except TypeError as e:
            logger.error(f"Page: {page_name} Action: [wait_ele_presence] Element：{loc}\n"
                         f"Msg:Wait element presence model:{model} is error. Please choose 'all, single'")
            raise e
        else:
            end_time = datetime.datetime.now()
            logger.info(f"Page: {page_name} Action: [wait_ele_presence] Element: {loc}\n"
                        f"Msg:presence successful,waiting time:{end_time - start_time}")
            return ele

    def open_web(self, url):
        self.driver.get(url)
        logger.info(f"Action: [open_web] Url: {url}")

    def find_ele(self, page_name, loc, timeout=30, polling=0.5, model="visible"):
        """find element

        :param page_name: page and object name
        :param loc: locators(by, loc)
        :param timeout: timeout(s) default=30s
        :param polling: polling(s) default=0,5s
        :param model: wait type default=visible
        :return: element object
        """
        try:
            if model == "visible":
                ele = self.wait_ele_visible(page_name, loc, timeout=timeout, polling=polling)
            elif model == "presence":
                ele = self.wait_ele_presence(page_name, loc, timeout=timeout, polling=polling)
            else:
                raise TypeError(f"Page: {page_name} Find element model: {model} error")
        except TypeError as e:
            logger.error(f"Page: {page_name} Action: [find_ele]  Element：{loc} Model: {model}\n"
                         f"Msg:Find element model: {model} error")
            raise e
        else:
            logger.info(f"Page: {page_name} Action: [find_ele] Element：{loc} Model: {model}\n"
                        f"Msg:Fount successful")
            return ele

    def click(self, page_name, loc, timeout=30, polling=0.5):
        """click element object

        :param page_name:  page and object name
        :param loc:  locators(by, loc)
        :param timeout:  timeout(s) default=30s
        :param polling:  polling(s) default=0,5s
        :return:  self
        """
        ele = self.find_ele(page_name, loc, timeout, polling)
        try:
            ele.click()
        except exceptions.ElementClickInterceptedException as e:
            logger.error(f"Page: {page_name} Action: [click] Element：{loc}\n"
                         f"Msg:click failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action: [click] Element：{loc}\n"
                        f"Msg:click successful")
            return self

    def send_keys(self, page_name, loc, *value, timeout=30, polling=0.5):
        """Simulates typing into the element.

        :param page_name:  page and object name
        :param loc:  locators(by, loc)
        :param value:  input data
        :param timeout:  timeout(s) default=30s
        :param polling:  polling(s) default=0,5s
        :return: self
        """
        ele = self.find_ele(page_name, loc, timeout, polling)
        try:
            ele.send_keys(*value)
        except exceptions.WebDriverException as e:
            logger.error(f"Page: {page_name} Action: [send_keys] Element：{loc}\n"
                         f"Msg:input failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action: [send_keys] Element：{loc} Input：{value}")
            return self

    def get_ele_attribute(self, page_name, loc, name, timeout=30, polling=0.5):
        """get element object attribute

        :param page_name:
        :param loc:
        :param name: attribute name, example: "class"
        :param timeout:
        :param polling:
        :return:
        """
        ele = self.find_ele(page_name, loc, timeout, polling)
        try:
            value = ele.get_attribute(name)
        except exceptions.NoSuchAttributeException as e:
            logger.error(f"Page: {page_name} Action: [get_ele_attribute] Element：{loc}\n"
                         f"Msg:Not exists attribute name: {name}! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action: [get_ele_attribute] Element: {loc}\n"
                        f"Msg:exists attribute name: {name} value: {value}")
            return value

    def get_text(self, page_name, loc, timeout=30, polling=0.1, text_type=None):
        """Get textbox data

        :param page_name:
        :param loc:
        :param timeout:
        :param polling:
        :param text_type:
        :return:
        """
        if text_type == "toast":
            loc = f"//*[contains(@text, '{loc}')]"
            loc = (MobileBy.XPATH, loc)
            ele = self.find_ele(page_name, loc, timeout=timeout, polling=polling, model="presence")
        else:
            ele = self.find_ele(page_name, loc, timeout=timeout, polling=polling)
        try:
            info = ele.text
        except exceptions.WebDriverException as e:
            logger.error(f"Page: {page_name} Action: [get_text] Element: {loc}\n"
                         f"Msg:Get text failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action: [get_text] Element: {loc} Get text successful: {info}")
            return info

    def get_toast(self, page_name, text, timeout=30, polling=0.1):
        """
        Get toast info
        :param page_name:
        :param text: contains keyword
        :param timeout:
        :param polling:
        :return:
        """
        info = self.get_text(page_name, text, timeout, polling, text_type="toast")
        return info

    @property
    def get_page_source(self):
        """
        Get current page source
        :return: Source
        """
        try:
            source = self.driver.page_source
        except exceptions.WebDriverException as e:
            logger.error(f"Action: [get_page_source]\n"
                         f"Msg:Get page source failed! Track: {e}")
            raise e
        else:
            logger.info("Action: [get_page_source]\n"
                        "Msg:Get page source successful")
            return source

    @property
    def get_handles(self):
        """
        Get all page handles
        :return: handles list
        """
        handles = self.driver.window_handles
        logger.info("Action: [get_handles]\n"
                    "Get all handle: {}".format(handles))
        return handles

    @property
    def get_handle(self):
        """
        Get current page handle
        :return: handle
        """
        handle = self.driver.current_window_handle
        logger.info("Action: [get_handles]\n"
                    "Get current handle: {}".format(handle))
        return handle


class WebBasicOperation(BasicOperation):
    """
    This class mainly stores web side operations
    """

    def switch_last_window(self, handles):
        """
        switch browser last tab
        :param handles: old handles
        :return:
        """
        try:
            WebDriverWait(self.driver, 30).until(ec.new_window_is_opened(handles))
            handles = self.get_handles
            self.driver.switch_to.window(handles[-1])
            current = self.driver.current_window_handle
            logger.info("Action: [switch_last_window]\n"
                        "switch window to {} successful".format(current))
        except exceptions.WebDriverException as e:
            logger.error(f"Action: [switch_last_window]\n"
                         f"switch window failed Track:{e}")
            self.capture_screen_shot("witch_window")
            raise e
        return self

    def switch_frame(self, page_name, loc, timeout=30, polling=0.5):
        """switch dom iframe

        :param page_name:  page and object name
        :param loc:  iframe index, iframe name, iframe locators(by, loc), iframe WebElement
        :param timeout:
        :param polling:
        :return: self
        """
        try:
            WebDriverWait(self.driver, timeout, polling).until(ec.frame_to_be_available_and_switch_to_it(loc))
        except exceptions.TimeoutException as e:
            logger.error(f"Page: {page_name} Action:[switch_frame] Element {loc}\n"
                         f"Msg:switch iframe failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[switch_frame] Element {loc}\n"
                        f"Msg:switch iframe successful")
            return self

    def __switch_alert(self, page_name, timeout=30, polling=0.5):
        """
        Waiting alert and switch
        :param page_name:
        :param timeout:
        :param polling:
        :return: alert object
        """
        try:
            WebDriverWait(self.driver, timeout, polling).until(ec.alert_is_present())
        except exceptions.TimeoutException as e:
            logger.error(f"Page: {page_name} Action:[switch_alert]\n"
                         f"Msg:Switch alert failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise exceptions.NoAlertPresentException(f"Page: {page_name} Switch alert failed!")
        else:
            logger.info(f"Page: {page_name}  Action:[switch_alert]\n"
                        f"Msg:switch alert successful")
            return self.driver.switch_to.alert

    def alert_accept(self, page_name, timeout=30, polling=0.5):
        """
        accept alert option
        :param page_name:
        :param timeout:
        :param polling:
        :return:
        """
        try:
            self.__switch_alert(page_name, timeout, polling).accept()
        except exceptions.WebDriverException as e:
            logger.error(f"Page: {page_name} Action:[alert_accept]\n"
                         f"Msg:alert accept failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[alert_accept] Msg:alert accept successful")
        return self

    def alert_dismiss(self, page_name, timeout=30, polling=0.5):
        """
        dismiss alert option
        :param page_name:
        :param timeout:
        :param polling:
        :return:
        """
        try:
            self.__switch_alert(page_name, timeout, polling).dismiss()
        except exceptions.WebDriverException as e:
            logger.error(f"Page: {page_name} Action:[alert_dismiss]\n"
                         f"Msg:alert dismiss failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[alert_dismiss] Msg:alert dismiss successful")
        return self

    def alert_send_keys(self, page_name, value, timeout=30, polling=0.5):
        """

        :param page_name:
        :param value: input alert input box data
        :param timeout:
        :param polling:
        :return:
        """
        try:
            self.__switch_alert(page_name, timeout, polling).send_keys(value)
        except exceptions.WebDriverException as e:
            logger.error(f"Page: {page_name} Action:[alert_send_keys]\n"
                         f"Msg:alert send keys:{value} failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[alert_send_keys]\n"
                        f"Msg:alert send keys:{value} successful")
        return self

    def scroll_screen(self, page_name, model, *target_ele):
        """Execute javascript scroll view

        :param page_name: Current view name
        :param model:
        :param target_ele: Scrolling to meet the target element will stop, only top bottom
        :return:
        """
        if model == "top":  # top
            js = "arguments[0].scrollIntoView()"
        elif model == "bottom":  # bottom
            js = "arguments[0].scrollIntoView(false)"
        elif model == "down":
            js = "window.scrollTo(0,document.body.scrollHeight)"
        elif model == "up":
            js = "window.scrollTo(document.body.scrollHeight,0)"
        else:
            logger.error("Choose javascript command model error! Please choose 'top bottom down up'")
            raise TypeError(f"Page: {page_name} Action:[scroll_screen] Msg:Model Error")
        try:
            if model in ("top", "bottom"):
                self.execute_js_script(js, target_ele)
            else:
                self.execute_js_script(js, target_ele)
        except exceptions.JavascriptException as e:
            logger.error(f"Page: {page_name} Action:[scroll_screen]\n"
                         f"Msg:Execute JS script Failed! Track:{e}")
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[scroll_screen] Msg:Execute JS script successful!")
        return self

    def sub_scroll(self, page_name, loc, value):
        """
        sub scroll bar
        :param page_name:
        :param loc: sub scroll bar locator
        :param value:
        :return:
        """
        element = self.find_ele(page_name, loc)
        self.execute_js_script(f"arguments[0].scrollTop = {int(value)}", element)
        logger.info(f"Page: {page_name} Action:[scroll_screen] Msg:Execute JS script successful!")

    def choose_select_options(self, page_name, loc, value, timeout=30, polling=0.5, model="text"):
        """choose select options

        :param loc:
        :param page_name:
        :param value:
        :param timeout:
        :param polling:
        :param model:
        :return:
        """
        ele = self.find_ele(page_name, loc, timeout, polling)
        try:
            options = Select(ele)
            if model == "index":
                options.select_by_index(value)
            elif model == "value":
                options.select_by_value(value)
            elif model == "text":
                options.select_by_visible_text(value)
            else:
                raise TypeError(f"Page: {page_name} Action:[choose_select_options] Element:{loc}\n"
                                f"Msg:Model is Error! Please choose 'index, value, text'")
        except exceptions.UnexpectedTagNameException as e:
            logger.error(f"Page: {page_name} Action:[choose_select_options] Element:{loc}\n"
                         f"Msg:The current element does not support select! Track:{e}")
            raise e
        return self

    def get_select_options(self, page_name, loc, timeout=30, polling=0.5):
        """
        Get select options
        :param page_name:
        :param loc:
        :param timeout:
        :param polling:
        :return: options: list
        """
        ele = self.find_ele(page_name, loc, timeout, polling)
        try:
            options = Select(ele)
            value = options.all_selected_options
        except exceptions.WebDriverException as e:
            logger.error(f"Page: {page_name} Action:[get_select_options] Element:{loc}\n"
                         f"Msg:Get select options failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[get_select_options]\n"
                        f"Msg:Select options value: {value}")
            return value

    def upload_file(self, file_path):
        """
        upload file
        :param file_path:
        :return:
        """
        time.sleep(2)
        pyautogui.write(file_path, _pause=1)
        pyautogui.press('enter', presses=2, interval=0.1, _pause=2)
        logger.info(f"Action:[upload_file] path:{file_path} Upload successful")
        return self

    def execute_js_script(self, command, target=None):
        if target:
            res = self.driver.execute_script(command, target)
        else:
            res = self.driver.execute_script(command)
        logger.info(f"Action:[execute_js_script] Msg: Command: {command} result: {res}")
        return res

    def get_session_storage(self, keyword):
        value = self.execute_js_script(f'return sessionStorage.getItem("{keyword}");')
        return value

    def set_session_storage(self, key, value):
        self.execute_js_script(f'sessionStorage.setItem("{key}", "{value}");')

    def get_all_storage(self):
        keys = self.execute_js_script("return Object.keys(sessionStorage)")
        values = dict()
        for k in keys:
            value = self.get_session_storage(k)
            values[k] = value
        return values

    def set_all_storage(self, **kwargs):
        for k, y in kwargs.items():
            self.set_session_storage(k, y)


class KeyMouse(Keys, ActionChains):
    """
    for mixin keyboard and mouse class
    """
    pass


class AppBasicOperation(BasicOperation):
    """
    This class mainly stores the mobile operation
    """

    def get_size(self, page_name, *loc, timeout=30, polling=0.5):
        """
        get full window or locator block size
        :param page_name:
        :param loc:
        :param timeout:
        :param polling:
        :return: size
        """
        try:
            if loc:
                size = self.find_ele(page_name, loc, timeout, polling).size
            else:
                size = self.driver.get_window_size()
        except exceptions.WebDriverException as e:
            if loc:
                logger.error(f"Page: {page_name} Action:[get_size] Element: {loc}\n"
                             f"Msg:get size failed! Track:{e}")
            else:
                logger.error(f"Page: {page_name} Action:[get_all_size]\n"
                             f"Msg:Get full window size failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            if loc:
                logger.info("Page: {} Action:[get_size] Element: {} Get size: {}".format(page_name, loc, size))
            else:
                logger.info("Page: {} Action:[get_all_size] Get window size: {}".format(page_name, size))
            return size

    def full_screen_scroll(self, page_name, direction="down", duration=300, timeout=30, polling=0.5):
        """page swipe

        :param page_name:
        :param direction: direction of the page, option: 'down', 'up', 'left', 'right'
        :param duration:
        :param timeout:
        :param polling:
        :return:
        """
        size = self.get_size(page_name, timeout=timeout, polling=polling)
        direction = direction.lower()
        if direction == "down":  # Page move down, swipe from down to up
            start_x, start_y, end_x, end_y = \
                size["width"] * 0.5, size["height"] * 0.7, size["width"] * 0.5, size["height"] * 0.1
        elif direction == "up":
            start_x, start_y, end_x, end_y = \
                size["width"] * 0.5, size["height"] * 0.2, size["width"] * 0.5, size["height"] * 0.8
        elif direction == "left":  # Page move left, swipe from left to right
            start_x, start_y, end_x, end_y = \
                size["width"] * 0.2, size["height"] * 0.5, size["width"] * 0.8, size["height"] * 0.5
        elif direction == "right":
            start_x, start_y, end_x, end_y = \
                size["width"] * 0.8, size["height"] * 0.5, size["width"] * 0.2, size["height"] * 0.5
        else:
            logger.error(f"Page: {page_name} Action:[full_screen_scroll]\n"
                         f"Msg:Scroll direction type Error value: {direction}")
            raise TypeError("Scroll direction type Error value: {}".format(direction))
        try:
            time.sleep(1)
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        except exceptions.WebDriverException as e:
            logger.error(f"Page: {page_name} Action:[full_screen_scroll]"
                         f"Msg:Scroll direction: {direction} failed! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[full_screen_scroll]\n"
                        f"Msg:Scroll direction: {direction} successful!")
            return self

    def full_screen_scroll_to_target(self, page_name, target_loc, keyword, wait_loc=None,
                                     model="down", duration=200, timeout=30, polling=0.5):
        """Swipe in specify the direction until you find the target

        :param page_name:
        :param target_loc:
        :param keyword: Used to match the target page source
        :param wait_loc: Waiting for location must be on every page view
        :param model: direction of the page, option: 'down', 'top', 'left', 'right'
        :param duration:
        :param timeout:
        :param polling:
        :return:
        """
        if wait_loc:
            self.wait_ele_visible(page_name, wait_loc, model="all")
        new = self.get_page_source
        old = ""
        times = 0
        try:
            while keyword not in new and new != old:
                self.full_screen_scroll(page_name, model, duration, timeout, polling)
                if wait_loc:
                    self.wait_ele_visible(page_name, wait_loc, model="all")
                old, new = new, self.get_page_source
                times += 1
                logger.debug(f"Page: {page_name} Action:[full_screen_scroll_to_target]\n"
                             f"Msg: Full screen scrolling times:{times}")
            if keyword not in new:
                logger.error(f"Page: {page_name} Action:[full_screen_scroll_to_target]\n"
                             f"Msg: keyword:{keyword} not found")
                raise exceptions.NoSuchElementException(f"keyword:{keyword} not found")
            ele = self.find_ele(page_name, target_loc, timeout, polling)
        except exceptions.NoSuchElementException as e:
            logger.error(f"Page: {page_name} Action:[full_screen_scroll_to_target]\n"
                         f"Msg:No keywords [{keyword}] found [{target_loc}] in screen scrolling! Track:{e}")
            self.capture_screen_shot(page_name)
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[full_screen_scroll_to_target]\n"
                        f"Msg: Find the target locator {target_loc}")
            return ele

    def zoom(self, page_name):
        """
        Zoom in page view, If it is a image, it will be enlarged ↖↘
        :param page_name:
        :return:
        """
        try:
            size = self.get_size(page_name)
            ma = MultiAction(self.driver)
            ta1 = TouchAction(self.driver)
            ta2 = TouchAction(self.driver)
            ta1.press(x=size["width"] * 0.5 - 1, y=size["height"] * 0.5 - 1).wait(200). \
                move_to(x=size["width"] * 0.1, y=size["height"] * 0.1).wait(200).release()
            ta2.press(x=size["width"] * 0.5 + 1, y=size["height"] * 0.5 + 1).wait(200). \
                move_to(x=size["width"] * 0.9, y=size["height"] * 0.9).wait(200).release()
            ma.add(ta1, ta2)
            ma.perform()
        except exceptions.WebDriverException as e:
            logger.error(f"Page: {page_name} Action:[zoom_in↖↘]\n"
                         f"Msg: zoom_in operation failed! Track:{e}")
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[zoom_in↖↘]\n"
                        f"Msg: zoom_in operation successful!")
        return self

    def pinch(self, page_name):
        """
        Pinch page view, If it is a image, it will be zoom ↘↖
        :param page_name:
        :return:
        """
        try:
            size = self.get_size(page_name)
            ma = MultiAction(self.driver)
            ta1 = TouchAction(self.driver)
            ta2 = TouchAction(self.driver)
            ta1.press(x=size["width"] * 0.2, y=size["height"] * 0.1).wait(200). \
                move_to(x=size["width"] * 0.5 - 1, y=size["height"] * 0.5 - 1).wait(200).release()
            ta2.press(x=size["width"] * 0.8, y=size["height"] * 0.7).wait(200). \
                move_to(x=size["width"] * 0.5 + 1, y=size["height"] * 0.5 + 1).wait(200).release()
            ma.add(ta1, ta2)
            ma.perform()
        except exceptions.WebDriverException as e:
            logger.error(f"Page: {page_name} Action:[zoom_out↘↖]\n"
                         f"Msg: zoom_out operation failed! Track:{e}")
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[zoom_out↘↖]\n"
                        f"Msg: zoom_out operation successful!")
        return self

    @property
    def get_contexts(self):
        """
        Get all context
        :return: contexts: list
        """
        contexts = self.driver.contexts
        logger.info("Get all context:{}".format(contexts))
        return contexts

    @property
    def get_current_context(self):
        """
        Get current activation page context
        :return: context: str
        """
        context = self.driver.context
        logger.info("Get current context:{}".format(context))
        return context

    def switch_context(self, page_name, class_name='android.webkit.WebView', index=-1, second=3):
        """
        switch context to WebView
        :param second: forced wait time(s)
        :param page_name:
        :param class_name:
        :param index:
        :return:
        """
        wait_loc = (MobileBy.CLASS_NAME, class_name)
        self.wait_ele_visible(page_name, wait_loc, timeout=10)
        time.sleep(int(second))  # Wait for H5 page to loading
        current = self.get_current_context
        contexts = self.get_contexts
        contexts.remove(current)
        context = contexts[index]
        try:
            self.driver.switch_to.context(context)
            if current == self.get_current_context:
                raise NoSuchContextException("Failed to switch context {}".format(context))
        except NoSuchContextException as e:
            self.capture_screen_shot(page_name)
            logger.error(f"Page: {page_name} Action:[switch_context]\n"
                         f"Msg: Failed to enter context:{self.get_current_context}. Track:{e}")
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[switch_context]\n"
                        f"Msg: Successful entry context:{self.get_current_context}")
            return self

    def switch_app(self, page_name, package, activity):
        """
        open other applications
        :param page_name:
        :param package: app package name
        :param activity: app activity name
        :return:
        """
        try:
            self.driver.start_activity(package, activity)
        except exceptions.WebDriverException as e:
            self.capture_screen_shot(page_name)
            logger.error(f"Page: {page_name} Action:[switch_app]\n"
                         f"Msg: Open app: {page_name} activity: {activity} Failed! Track:{e}")
            raise e
        else:
            logger.info(f"Page: {page_name} Action:[switch_app]\n"
                        f"Msg: Open app: {page_name} activity: {activity} Successful!")
            return self

    def switch_page_handle(self, page_name, keyword):
        """
        switch WebView handle
        :param page_name:
        :param keyword:
        :return:
        """
        handles = self.get_handles
        try:
            for handle in handles:
                self.driver.switch_to.window(handle)
                logger.debug(f"Page: {page_name} Action:[switch_page_handle]\n"
                             f"Msg: Switch to handle:{handle}")
                if keyword in self.get_page_source:
                    break
            if keyword not in self.get_page_source:
                raise exceptions.NoSuchElementException("No such keyword:{} in page source:{}".
                                                        format(keyword, self.get_page_source))
        except exceptions.NoSuchElementException as e:
            handle = self.get_handle
            self.capture_screen_shot(page_name)
            logger.error(f"Page: {page_name} Action:[switch_page_handle]\n"
                         f"Msg: Switch to handle:{handle}, keyword not found! Track:{e}")
            raise e
        else:
            handle = self.get_handle
            logger.info(f"Page: {page_name} Action:[switch_page_handle]\n"
                        f"Msg: Switch to handle:{handle} keyword found")
            return self

    def always_allow(self, page_name, n=6, mode="1"):
        """
        Permission allowed
        :param page_name:
        :param n: times
        :return:
        """
        loc = (MobileBy.ANDROID_UIAUTOMATOR, 'textContains("允许").clickable(true)')
        switch = self.get_text("permission", loc)
        while switch and n <= 6:
            n -= 1
            if mode == "1":
                self.driver.press_keycode(66)
                time.sleep(0.8)
            else:
                self.click("permission", loc)
                time.sleep(0.8)
            try:
                switch = self.get_text("permission", loc, timeout=3)
            except exceptions.TimeoutException:
                logger.info(f"Page: {page_name} Action:[always_allow] \n Msg: No '允许' on current page")
                break

    def camera(self, n=3):
        """
        entry camera operate
        :return:
        """
        time.sleep(2)
        self.driver.press_keycode(27)  # 拍照键
        time.sleep(5)  # 部分手机拍照会倒计时
        for i in range(n):
            time.sleep(2)
            self.driver.press_keycode(22)  # 向右, 默认三次
        self.driver.press_keycode(66)  # 回车键
        logger.info("Action:[camera] Msg: operate successful")
