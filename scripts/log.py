
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)


LOG_LEVEL_DEBUG = 0
LOG_LEVEL_WARNING = 1
LOG_LEVEL_ERROR = 2

LOG_LEVEL = LOG_LEVEL_DEBUG

def log_print(level, msg):
    if LOG_LEVEL <= level:
        print(msg)
