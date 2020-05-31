from hashids import Hashids
import random

def generate_hashid():
    hash_ids = Hashids(
        salt='E-Revenue',
        min_length=8
    )
    hash_id = hash_ids.encode(random.randint(1, 10000000))
    return hash_id.upper()