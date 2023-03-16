import inspect
import logging
import datetime

class customLogen:
    now = datetime.datetime.now()
    current_date = now.strftime("%Y_%m_%d_T%H:%M:%S")
    log_file = f"./Report/Logs/automation_{current_date}.log"

    def customLogger(self, logger_name: str, log_level=logging.DEBUG):
        # Set class/method name from where it is called
        # logger_name = inspect.stack()[1][3]
        # print(inspect.stack())
        # Create logger
        logger = logging.getLogger(logger_name)
        # logger = logging.getLogger()
        # logger = logging.getLogger(customLogen.__name__)
        logger.setLevel(log_level)
        # Create console/file handler and set the log level
        file_handler = logging.FileHandler(filename=self.log_file, mode="a")
        # Create formatter - how you want your logs to be formatted
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        # Add formatter to console of file handler
        file_handler.setFormatter(formatter)
        # Add console handler to logger
        logger.addHandler(file_handler)

        # ----------------------------------
        # # Stream Handler -> Logs to console
        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(formatter)
        # logger.addHandler(stream_handler)


        return logger
        # print(logger_name)

# log = customLogen()
# customLogen.customLogger(logging.INFO)