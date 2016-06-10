import uuid


def generate_client_secret():
    return uuid.uuid4().hex


def generate_code():
    return uuid.uuid4().hex
