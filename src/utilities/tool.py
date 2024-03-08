import uuid


def get_client_id(prefix=""):
    return prefix + str(uuid.uuid4())


def pad_string(input_string, max_len=38):
    padded_string = input_string.ljust(max_len)
    return padded_string
