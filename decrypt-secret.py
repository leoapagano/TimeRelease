import base64
import hashlib
import json
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from tqdm import tqdm


def base64_to_byte_str(base64_string):
	"""Converts a base64 string to its byte string representation."""
	return base64.b64decode(base64_string.encode('ASCII'))


def decrypt_secret(enc_package):
	base = enc_package["base"]
	modulus = enc_package["modulus"]
	iterations = enc_package["iterations"]
	secret_iv = base64_to_byte_str(enc_package["secret_iv"])
	encrypted_secret = base64_to_byte_str(enc_package["encrypted_secret"])
	key_iv = base64_to_byte_str(enc_package["key_iv"])
	encrypted_key = base64_to_byte_str(enc_package["encrypted_key"])

	# Compute puzzle result r
	start_time = time.time()
	r = base
	for _ in tqdm(range(iterations), desc="Unlocking", unit="iters"):
		r = pow(r, 2, modulus)
	end_time = time.time()
	print(f"Completed in {end_time - start_time:.2f} seconds") # move later

	# Derive AES key from r
	derived_key = hashlib.sha256(str(r).encode()).digest()[:16]

	# Decrypt AES key
	cipher2 = AES.new(derived_key, AES.MODE_CBC, iv=key_iv)
	aes_key = unpad(cipher2.decrypt(encrypted_key), AES.block_size)

	# Decrypt secret
	cipher = AES.new(aes_key, AES.MODE_CBC, iv=secret_iv)
	secret = unpad(cipher.decrypt(encrypted_secret), AES.block_size)
	return secret


if __name__ == "__main__":
	# Read from timerelease.json
	with open('timerelease.json', 'r') as f:
		enc_package = json.load(f)

	print(f"SECRET: {decrypt_secret(enc_package).decode()}")

