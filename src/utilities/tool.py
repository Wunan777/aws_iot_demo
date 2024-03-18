import uuid
import sys
from time import sleep


def get_client_id(prefix=""):
    return prefix + str(uuid.uuid4())


def pad_string(input_string, max_len=37):
    padded_string = input_string.ljust(max_len)
    return padded_string


def mock_loading_n_second(second, loading_msg):
    duration = 0
    while True:
        for frame in "|/-\\":
            print(f"\r{loading_msg} {frame}", end="", flush=True)
            sleep_interval = 0.2
            sleep(sleep_interval)
            duration = duration + sleep_interval

            if duration > second:
                return
