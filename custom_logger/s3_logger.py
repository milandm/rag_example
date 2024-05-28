import logging
from custom_logger.s3_rotating_file_handler import S3UploadRotatingFileHandler

class S3Logger:
    def __init__(self, logger_name='s3_rotating_logger'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        # Use our custom handler, which will push to S3 when logs rotate
        s3_handler = S3UploadRotatingFileHandler(filename='app.log', bucket='your-s3-bucket-name', maxBytes=1*1024*1024, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        s3_handler.setFormatter(formatter)
        self.logger.addHandler(s3_handler)

    def getLogger(self):
        return self.logger