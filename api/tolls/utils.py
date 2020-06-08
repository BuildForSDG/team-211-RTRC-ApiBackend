from hashids import Hashids
import random
from api.tolls.models import Toll

def generate_hashid():
    hash_ids = Hashids(
        salt='E-Revenue',
        min_length=8
    )
    hash_id = hash_ids.encode(random.randint(1, 10000000))
    return hash_id.upper()

def unique_hashid():
    reference = generate_hashid()
    while Toll.objects.filter(reference=reference).exists():
        reference = generate_hashid()
    return reference
