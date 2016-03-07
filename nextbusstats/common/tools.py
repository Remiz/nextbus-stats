import time


def is_valid_time_format(time_str):
    # Validate a time, ex: 4:00am
    try:
        time.strptime(time_str, '%I:%M%p')
        return True
    except ValueError:
        return False
