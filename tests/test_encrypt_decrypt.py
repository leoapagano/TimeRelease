from TimeRelease import encrypt_secret, decrypt_secret

def test_hello_world():
	"""
	Very basic test case. Just ensures that an input, when encrypted and decrypted,
	produces the same output that it started with.
	"""
	input = b"hello world"
	encrypted = encrypt_secret(input, 2 ** 16, logging=False)
	decrypted = decrypt_secret(encrypted, logging=False)
	assert decrypted == b"hello world"
