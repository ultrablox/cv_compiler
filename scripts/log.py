
LOG_LEVEL_DEBUG = 0
LOG_LEVEL_WARNING = 1
LOG_LEVEL_ERROR = 2

LOG_LEVEL = LOG_LEVEL_DEBUG

def log_print(level, msg):
    if LOG_LEVEL <= level:
        print(msg)
