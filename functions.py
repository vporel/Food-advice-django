
from hashlib import sha1

"""
    Hashage d'une chaine en sha1
"""
def hashPassword(string):
    return sha1(string.encode("utf-8")).hexdigest()