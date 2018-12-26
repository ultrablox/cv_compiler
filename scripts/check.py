
def check_always(condition, msg = ''):
  if not condition:
    raise AssertionError(msg)
        