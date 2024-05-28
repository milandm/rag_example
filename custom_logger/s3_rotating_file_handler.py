import boto3
from logging.handlers import RotatingFileHandler


class S3UploadRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, bucket, aws_access_key_id=None, aws_secret_access_key=None, maxBytes=5 * 1024 * 1024,
                 backupCount=5):
        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount)
        self.bucket = bucket
        self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    def doRollover(self):
        # Push the current log to S3 before performing the rollover
        self.stream.close()
        self.s3.upload_file(self.baseFilename, self.bucket, f"logs/{self.baseFilename}")

        # Call the parent class's doRollover to perform file rotation
        super().doRollover()