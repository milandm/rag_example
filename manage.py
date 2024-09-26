import os
import sys

# import pydevd_pycharm
#
# import pydevd

import time

from custom_logger.universal_logger import UniversalLogger

# # "host.docker.internal",
# time.sleep(30)
# pydevd_pycharm.settrace('localhost',
# port=5678,
# stdoutToServer=True,
# stderrToServer=True)








if __name__ == "__main__":
    logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_crud.settings")

    logger.info("__main__")

    # time.sleep(30)
    # try:
    #      pydevd_pycharm.settrace(
    #          "172.17.0.1",
    #          port=5678,
    #          suspend=False,
    #          stdoutToServer=True,
    #          stderrToServer=True,
    #      )
    # except Exception as e:
    #     logger.error("pydevd_pycharm " + (str(e)))
    # logger.info("pydevd_pycharm successfully initialized")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)



