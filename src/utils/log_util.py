import logging
import inspect
import time
from src.constants import LOGGING_LEVEL

logging.basicConfig(
    level=getattr(logging, LOGGING_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s - Line: %(lineno)d',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("application.log"),
        logging.StreamHandler()
    ]
)

class Logger:
    @staticmethod
    def _get_caller_info():
        """Get the caller's file name and line number, skipping the Logger class frame."""
        frame = inspect.currentframe()
        # Move up the stack to find the caller's frame
        while frame:
            frame = frame.f_back
            # Check if the frame is not from the Logger class
            if frame and frame.f_code.co_filename != __file__:
                return frame.f_code.co_filename.split('/')[-1], frame.f_lineno  # Get the file name and line number
        return "Unknown", 0

    @staticmethod
    def log_info(message):
        if LOGGING_LEVEL == "INFO":  # Only log if the level is DEBUG
            file_name, line_number = Logger._get_caller_info()
            logging.info(f"{message} - {file_name} - Line: {line_number}")

    @staticmethod
    def log_warning(message):
        if LOGGING_LEVEL in ["DEBUG", "WARNING"]:  # Log if level is DEBUG or WARNING
            file_name, line_number = Logger._get_caller_info()
            logging.warning(f"{message} - {file_name} - Line: {line_number}")

    @staticmethod
    def log_error(message, exc_info=False):
        file_name, line_number = Logger._get_caller_info()
        logging.error(f"{message} - {file_name} - Line: {line_number}", exc_info=exc_info)

    @staticmethod
    def log_debug(message):
        if LOGGING_LEVEL == "DEBUG":  # Only log if the level is DEBUG
            file_name, line_number = Logger._get_caller_info()
            logging.debug(f"{message} - {file_name} - Line: {line_number}")

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
