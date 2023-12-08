import random, string


def generate_unique_id(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))
