#utils for utilities. Mainly just useful functions for later use
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password(input_password, stored_hashed_password):
    return hash_password(input_password) == stored_hashed_password
