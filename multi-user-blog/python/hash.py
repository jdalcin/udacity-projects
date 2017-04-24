"""Methods to hash passwords and cookies  and validate logins and cookies using the Sha256 hashing algorithm"""

import random
import string
import hashlib

def make_salt():
	return ''.join(random.choice(string.letters) for letter in range(5))

def make_cookie_secure(name):
	if name is None:
		return None

	secret_word = 'wubbalubbadubdub' # ensures user cannot guess the hash using simply a name
	hash_cookie = hashlib.sha256(''.join([name, secret_word])).hexdigest()
	return "%s-%s" % (name, hash_cookie)

def validate_cookie(hashed_cookie):
	if hashed_cookie is None or not '-' in hashed_cookie:
		return None

	name = hashed_cookie.split('-')[0]
	hashed_name = hashed_cookie.split('-')[1]
	if make_cookie_secure(name).split('-')[1] == hashed_name:
		return name
	else:
		return None


def make_password_hash(name, password):
	if name is None or password is None:
		return None

	salt = make_salt()
	hashed = hashlib.sha256(''.join([name.lower(), password, salt])).hexdigest()
	return "%s-%s" % (hashed, salt) 

def validate_login(name, password, salt_hashed_string):
	if name is None or password is None or salt_hashed_string is None or not '-' in salt_hashed_string:
		return None

	hashing = salt_hashed_string.split('-')[0]
	salt = salt_hashed_string.split('-')[1]
	hash_check = hashlib.sha256(''.join([name.lower(), password, salt])).hexdigest()
	return hashing == hash_check



