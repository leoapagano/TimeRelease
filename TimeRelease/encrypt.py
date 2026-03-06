import hashlib
import random

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from sympy import nextprime

from .b64utils import byte_str_to_base64


def encrypt_secret(secret, iterations, logging=True):
	"""
	Given a byte string `secret`, encrypt_secret() applies `iterations` iterations to it, "encrypting" it.
	If `logging` (defaults to True) is set to True, extra debug information is printed.
	"""
	# Create new (symmetric) AES key and encrypt secret with it
	if logging:
		print("Generating encryption key...")
	aes_key = get_random_bytes(16)
	cipher = AES.new(aes_key, AES.MODE_CBC)
	secret_iv = cipher.iv
	encrypted_secret = cipher.encrypt(pad(secret, AES.block_size))

	# Time-lock puzzle setup
	# Generate N = p * q
	if logging:
		print("Preparing time lock...")
	p = nextprime(random.getrandbits(512))
	q = nextprime(random.getrandbits(512))
	modulus = p * q

	# Puzzle: compute r = base^(2^iterations) mod modulus
	base = random.randint(2, modulus - 1)
	r = pow(base, pow(2, iterations, (p - 1) * (q - 1)), modulus)

	# Derive AES key from r (e.g. using SHA256)
	if logging:
		print("Deriving AES key from time lock...")
	derived_key = hashlib.sha256(str(r).encode()).digest()[:16]

	# Encrypt AES key with derived key
	if logging:
		print("Encrypting derived key...")
	cipher2 = AES.new(derived_key, AES.MODE_CBC)
	key_iv = cipher2.iv
	encrypted_key = cipher2.encrypt(pad(aes_key, AES.block_size))

	# Stash stuff needed to decrypt later
	return {
		"base": base,
		"modulus": modulus,
		"iterations": iterations,
		"secret_iv": byte_str_to_base64(secret_iv),
		"encrypted_secret": byte_str_to_base64(encrypted_secret),
		"key_iv": byte_str_to_base64(key_iv),
		"encrypted_key": byte_str_to_base64(encrypted_key),
	}
