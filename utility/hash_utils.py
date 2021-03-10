import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    """Hashes the block
    Arguments:
        :block: block that should be hashed
    """
    hashable_block = block.__dict__.copy()
    print(block)
    hashable_block['transaction'] = [tx.to_ordered_dict() for tx in hashable_block["transaction"]]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
