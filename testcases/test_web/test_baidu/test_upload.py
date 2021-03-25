import pytest

from pageobject.web.baidu.upload_page import UploadImage


@pytest.mark.baidu
class TestUpload:

    def test_upload(self, driver):
        obj = UploadImage(driver)
        obj.click_button()
        target = obj.get_target()
        assert target == "相似图片"

    def test_upload1(self, driver):
        obj = UploadImage(driver)
        obj.click_button()
        target = obj.get_target()
        assert target == "相似图片"

    def test_upload2(self, driver):
        obj = UploadImage(driver)
        obj.click_button()
        target = obj.get_target()
        assert target == "相似图片"
