import uuid


def get_client_id(prefix=""):
    return prefix + str(uuid.uuid4())
