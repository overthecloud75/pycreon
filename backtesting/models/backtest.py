import logging

from commons.custommodel import CustomModel


class BackTesting(CustomModel):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info('%s start' % __name__)
        self.codeInfoListInDB = self.codeInfoInDB()

    def test(self):
        for codeInfo in self.codeInfoListInDB:
            pass