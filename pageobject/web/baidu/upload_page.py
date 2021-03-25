from common.basicoperation import WebBasicOperation
from pagelocators.web.baidu.baidu_upload_loc import UploadLoc
from pagedatas.web.baidu.baidu_upload import BaiDuUpload


class UploadImage(WebBasicOperation):

    def click_button(self):
        self.click("upload_button", UploadLoc.button)
        self.click("file_button", UploadLoc.upload)
        self.upload_file(BaiDuUpload.path)

    def get_target(self):
        return self.get_text("get_title", loc=UploadLoc.content, timeout=5)
