import logging
import time

# Configure logging with a custom format that includes the timestamp in UTC
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Customize the date format as needed
)

class Logger:
    @staticmethod
    def log_info(message):
        logging.info(message)

    @staticmethod
    def log_warning(message):
        logging.warning(message)

    @staticmethod
    def log_error(message, exc_info=False):
        logging.error(message, exc_info=exc_info)

    @staticmethod
    def log_debug(message):
        logging.debug(message)
        
    @staticmethod
    def error(message, exc_info=False):
        logging.error(message, exc_info=exc_info)
    
    @staticmethod
    def warning(message):
        logging.warning(message)
    
    @staticmethod
    def info(message):
        logging.info(message)


# Custom function to override the default time function to return UTC time
def utc_time(*args):
    return time.gmtime()  # Return struct_time in UTC

# Set the logging formatter to use UTC time
logging.Formatter.converter = utc_time
