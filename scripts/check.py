
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)


def check_always(condition, msg = ''):
  if not condition:
    raise AssertionError(msg)
        
